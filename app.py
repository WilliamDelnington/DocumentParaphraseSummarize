from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, send
from werkzeug.utils import secure_filename
from DPS_2 import read_and_analyze
import os

app = Flask(__name__)
socketio = SocketIO(app)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "doc", "txt"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return "." in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("upload.html")

@socketio.on('message')
def handle_message(message):
    print('Received message:', message)
    send(message, broadcast=True)  # Broadcast the message to all clients

@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files["file"]

    if file.name == "":
        return redirect(request.url)
    
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        return "File uploaded successfully"
    
    return "Invalid file type."

if __name__ == "__main__":
    app.run(debug=True)