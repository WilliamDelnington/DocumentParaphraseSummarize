from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_socketio import SocketIO, send
from werkzeug.utils import secure_filename
from ModelAnalyzing import read_and_analyze
import json
import os
import re
import random
import tempfile
import traceback
import HandleTemporaryFiles

app = Flask(__name__)
app.secret_key = os.getenv("SESSION_SECRET_KEY")
socketio = SocketIO(app)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "doc", "txt"}
JSON_DATA_PATH = "./data.json"

WORD_LIMIT_PATTERN = r"\d+\swords"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

def allowed_file(filename):
    return "." in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def write_data_to_json_file(file_path, data):
    """
    Add additional data into json array.
    """
    if os.stat(file_path).st_size == 0:
        json_data = []
    else:
        with open(file_path, "r") as file:
            json_data = json.load(file)

    json_data.append(data)

    with open(file_path, "w") as file:
        json.dump(json_data, file, indent=4)

# Setup main route for the web.
@app.route("/")
def index():
    return render_template("upload.html")

# Route for creating a bot message object
@app.route('/chat', methods=['POST'])
def chat():
    with open("./responses.json") as f:
        dataset = json.load(f)
    # Get user's message.
    user_message = request.form.get('message', '').strip()
    # Get the selected model.
    model = request.form.get("model", "t5-small")

    default_yes_response = {}
    other_file_response = "Sorry. I don't support this file."
    task = None

    # Search in the message whether the user request the task limitations.
    # If the re.search function returns None or error, then there aren't any word limitations
    try:
        word_limit = int(re.search(WORD_LIMIT_PATTERN, user_message).group().split(" ")[0])
        print(word_limit)
    except:
        print("No word limit found")
        word_limit = 250

    for data in dataset:
        if data["intent"]["tags"] == "summarize":
            # Create a regex string with metacharacters to match summarization purpose
            summarize_patterns = data["intent"]["patterns"][0]
            default_yes_response["summarize"] = random.choice(data["responses"]) + f"in {word_limit} words"

        elif data["intent"]["tags"] == "paraphrase":
            # Create a regex string with metacharacters to match paraphrasing purpose
            paraphrase_patterns = data["intent"]["patterns"][0]
            default_yes_response["paraphrase"] = random.choice(data["responses"]) + f"in {word_limit} words"

        elif data["intent"]["tags"] == "read":
            # Create a regex string with metacharacters for reading purpose.
            read_patterns = data["intent"]["patterns"][0]
            default_yes_response["read"] = random.choice(data["responses"])

        elif data["intent"]["tags"] == "default":
            default_no_response = random.choice(data["responses"])

    # Defining tasks for the model
    if re.search(summarize_patterns, user_message):
        if model.startswith("t5"):
            task = "summarize"
        else:
            task = "Summarize this text: "

    elif re.search(paraphrase_patterns, user_message):
        if model.startswith("t5"):
            task = "paraphrase"
        else:
            task = "Paraphrase this text: "

    elif re.search(read_patterns, user_message):
        task = "read"

    # Check whether a task is defined, otherwise makes the chatbot like having
    # a normal conversation.
    if task: 
        if request.files["file"]:
            file = request.files["file"]
            filename = file.filename.lower()

            # Categorize the file and read the contents from the supported file.
            try:
                text = HandleTemporaryFiles.read_file(file, filename)
            except:
                print(traceback.format_exc())
                return jsonify({"response": other_file_response}), 201
            
            if task == "summarize" or task == "paraphrase":
                analysis, metrics = read_and_analyze(text, model, task, word_limit)
                analysis["tokenization"]["input_text"] = analysis["tokenization"]["input_text"] if len(analysis["tokenization"]["input_text"]) < 150 else analysis["tokenization"]["input_text"][:150] + "..."

                # After finishing analysis, write the data into json file.

                write_data_to_json_file(JSON_DATA_PATH, {
                    "filename": filename,
                    "analysis": analysis,
                    "metrics": metrics
                })
                answer_text = analysis["generation"]["generated_text"]

            elif task == "Summarize this text: ":
                analysis, metrics = read_and_analyze(text, model, task, word_limit)
                analysis["tokenization"]["input_text"] = analysis["tokenization"]["input_text"] if len(analysis["tokenization"]["input_text"]) < 150 else analysis["tokenization"]["input_text"][:150] + "..."
                write_data_to_json_file(JSON_DATA_PATH, {
                    "filename": filename,
                    "analysis": analysis,
                    "metrics": metrics
                })
                answer_text = analysis["generation"]["generated_text"]
                return jsonify({"response": f"{default_yes_response['summarize']}\n{answer_text}"})
            
            elif task == "Paraphrase this text: ":
                analysis, metrics = read_and_analyze(text, model, task, word_limit)
                analysis["tokenization"]["input_text"] = analysis["tokenization"]["input_text"] if len(analysis["tokenization"]["input_text"]) < 150 else analysis["tokenization"]["input_text"][:150] + "..."
                answer_text = analysis["generation"]["generated_text"]
                write_data_to_json_file(JSON_DATA_PATH, {
                    "filename": filename,
                    "analysis": analysis,
                    "metrics": metrics
                })
                return jsonify({"response": f"{default_yes_response['paraphrase']}\n{answer_text}"})
            
            else:
                answer_text = text
            

            return jsonify({"response": f"{default_yes_response[task]}\n{answer_text}"}), 201
        else:
            return jsonify({"response": default_no_response}), 201
    else:
        for data in dataset:
            try:
                if any(
                    re.search(data["intent"]["patterns"][i], user_message)
                    for i in range(len(data["intent"]["patterns"]))
                    ):
                    return jsonify({"response": random.choice(data["responses"])})
            except:
                print(data["intent"]["patterns"], dataset.index(data))
                print(traceback.print_exc())
                raise Exception("Error detected")
        return jsonify({"response": f"{default_no_response}"}), 201

if __name__ == "__main__":
    app.run(debug=True)