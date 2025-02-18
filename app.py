from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_socketio import SocketIO, send
from werkzeug.utils import secure_filename
from DPS_2 import read_and_analyze
from readfile import ReadFile
import json
import os

with open("responses.json") as f:
    dataset = json.load(f)

app = Flask(__name__)
app.secret_key = os.getenv("SESSION_SECRET_KEY")
socketio = SocketIO(app)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "doc", "txt"}

NEGATIVE_WORDS = ["no", "don't", "without", "doesn't", "not", "isn't", "aren't", "wasn't", "weren't"]
TASKS = ["summarize", "paraphrase", "greetings", "questioning"]

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return "." in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("upload.html")

# @socketio.on('message')
# def handle_message(message):
#     print('Received message:', message)
#     send(message, broadcast=True)  # Broadcast the message to all clients

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form.get('message', '').strip()

    default_response = "Sorry. I don't understand. I'm not supported to answer this question."
    containing_negatives = [word for word in NEGATIVE_WORDS if word in user_message]
    
    return jsonify({"response": default_response}), 201

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
    
def analyze(file_path, model="t5-base", task="summarize"):
    reader = ReadFile(file_path)
    text = reader.read()

    analysis, metrics = read_and_analyze(text, model, task)

    return analysis, metrics

if __name__ == "__main__":
    app.run(debug=True)