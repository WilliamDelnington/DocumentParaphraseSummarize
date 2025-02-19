from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_socketio import SocketIO, send
from werkzeug.utils import secure_filename
from DPS_2 import read_and_analyze
import json
import os
import fitz
import docx
import io
import re
import random

with open("responses.json") as f:
    dataset = json.load(f)

app = Flask(__name__)
app.secret_key = os.getenv("SESSION_SECRET_KEY")
socketio = SocketIO(app)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "doc", "txt"}

WORD_LIMIT_PATTERN = r"\d+\swords"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return "." in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("upload.html")

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form.get('message', '').strip()

    default_yes_response = {}
    other_file_response = "Sorry. I don't support this file."
    task = None

    # If the re.search function returns None or error, then there aren't any word limitations
    try:
        word_limit = int(re.search(WORD_LIMIT_PATTERN, user_message).group().split(" ")[0])
    except:
        word_limit = None

    for data in dataset:
        if data["intent"]["tags"] == "summarize":
            # Create a regex string with metacharacters to match summarization purpose
            summarize_patterns = r"\b(" + "|".join(data["intent"]["patterns"]) + r")\b"
            default_yes_response["summaize"] = random.choice(data["responses"])
        elif data["intent"]["tags"] == "paraphrase":
            # Create a regex string with metacharacters to match paraphrasing purpose
            paraphrase_patterns = r"\b(" + "|".join(data["intent"]["patterns"]) + r")\b"
            default_yes_response["paraphrase"] = random.choice(data["responses"])
        elif data["intent"]["tags"] == "read":
            read_patterns = r"\b(" + "|".join(data["intent"]["patterns"]) + r")\b"
            default_yes_response["read"] = random.choice(data["responses"])
        elif data["intent"]["tags"] == "default":
            default_no_response = random.choice(data["responses"])

    # Defining tasks for the model
    if re.search(summarize_patterns, user_message):
        task = "summarize"

    elif re.search(paraphrase_patterns, user_message):
        task = "paraphrase"

    elif re.search(read_patterns, user_message):
        task = "read"

    if task: 
        if request.files["file"]:
            file = request.files["file"]
            filename = file.filename.lower()

            if filename.endswith(".txt"):
                text = file.read().decode("utf-8")

            elif filename.endswith(".docx"):
                doc = docx.Document(io.BytesIO(file.read()))
                text = "\n".join([p.text for p in doc.paragraphs])
            
            elif filename.endswith(".pdf"):
                pdf = fitz.open(stream=file.stream, filetype="pdf")
                text = "\n".join([p.get_text() for p in pdf])

            else:
                return jsonify({"response": other_file_response}), 201
            
            if task == "summarize" and task == "paraphrase":
                analysis, metrics = read_and_analyze(text, request.form.get("model", "t5-small"), task)
            else:
                analysis = text
            
            return jsonify({"response": f"{default_yes_response}\n{analysis}"}), 201
        else:
            return jsonify({"response": default_no_response}), 201
    else:
        for data in dataset:
            if user_message in data["intent"]["patterns"]:
                return jsonify({"response": random.choice(data["responses"])})
        return jsonify({"response": f"{default_no_response}"}), 201

@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return jsonify({"response": "No file uploaded"}), 400
    
    file = request.files["file"]

    if file.name == "":
        return jsonify({"response": "Name was not specified"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        try:
            file.save(filepath)
            session["file"] = filepath
            return jsonify({"response": f"File was uploaded: {filename}"}), 200
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({"response": f"Uploading failed: {e}"}), 500
    
    return jsonify({"response": "Invalid file type."}), 400

@app.route('/reset', methods=['DELETE'])
def reset():
    if not session.get("file", None):
        return jsonify({"response": "No file occurred"}), 400
    
    try:
        os.remove(session["file"])
        session.pop("file")
        return jsonify({"response": "File was successfully removed"}), 204
    except Exception as e:
        return jsonify({"response": "Error removing file: {e}"}), 400

if __name__ == "__main__":
    app.run(debug=True)