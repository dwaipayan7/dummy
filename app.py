from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from resumeParsing import matchingPer
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf'}

with open('job_desc.txt', 'r') as file:
        # Read the content
        job_desc = file.read()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def display_resumes():
    resumes = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.endswith(".pdf"):
            resume_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            matchPer = matchingPer(resume_path, job_desc)
            resumes.append({
                "Name": matchPer['name'],
                "Percentage": matchPer['per']
            })
    return jsonify(resumes)

@app.route('/', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No file part"}), 400

    resume_file = request.files['resume']

    if resume_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if resume_file and allowed_file(resume_file.filename):
        filename = secure_filename(resume_file.filename)
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        resume_file.save(resume_path)
        return jsonify({"message": "File uploaded successfully"}), 200
    else:
        return jsonify({"error": "File type not allowed"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=3000)