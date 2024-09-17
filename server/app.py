import os

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from functions import create_video

app = Flask(__name__)
CORS(app)  # Enable CORS to allow communication between frontend and backend

# Set the upload folder path for PDFs
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Set the folder path for MP4 videos
VIDEO_FOLDER = 'vids'

# test
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello from the server!"})

# Route for handling PDF file uploads
@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['pdf']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    print(file.filename)

    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        
        create_video(file_path)
        
        return jsonify({"message": "PDF uploaded successfully", "file": file.filename}), 200
    else:
        return jsonify({"error": "Invalid file type. Only PDFs are allowed."}), 400

@app.route('/get_videos')
def get_videos():
    video_dir = os.path.join(os.path.dirname(__file__), 'vids')
    try:
        files = os.listdir(video_dir)
        return jsonify(files)
    except OSError as e:
        app.logger.error(f'Error reading video directory: {e}')
        return jsonify({'error': 'Error reading video directory'}), 500

# Route to serve MP4 video file
@app.route('/get_video/<filename>', methods=['GET'])
def get_video(filename):
    try:
        return send_from_directory(VIDEO_FOLDER, filename)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
