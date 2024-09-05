from flask import Flask, request, jsonify, send_from_directory
import os
import whisper
from flask_cors import CORS
import subprocess
from werkzeug.utils import secure_filename
import shutil
from datetime import datetime
import json

app = Flask(__name__, static_folder='./react-frontend/build', static_url_path='/')
CORS(app)

# Ensure the uploads and transcripts directories exist
if not os.path.exists('uploads'):
    os.makedirs('uploads')
if not os.path.exists('transcripts'):
    os.makedirs('transcripts')


def is_safe_path(basedir, path, follow_symlinks=True):
    # Check if the path is safe to access
    if follow_symlinks:
        return os.path.realpath(path).startswith(basedir)
    return os.path.abspath(path).startswith(basedir)


@app.route('/api/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    # Sanitize the filename
    filename = secure_filename(filename)
    file_path = os.path.join('uploads', filename)

    # Ensure the path is safe to prevent directory traversal
    if not is_safe_path(os.path.join(app.root_path, 'uploads'), file_path):
        return jsonify({'message': 'Invalid file path'}), 400

    # Delete the file if it exists
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({'message': 'File deleted successfully'})
        else:
            return jsonify({'message': 'File not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    
@app.route('/api/files', methods=['GET'])
def list_files():
    files = os.listdir('uploads')
    return jsonify({"files": files})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    model_size = request.form.get('model_size', 'base')

    # Remove file extension and add a new one for consistency
    filename_without_extension = os.path.splitext(uploaded_file.filename)[0]
    audio_file_path = os.path.join('uploads', filename_without_extension + '.wav')
    transcript_file_path = os.path.join('transcripts', filename_without_extension + '_transcribe.txt')

    # Save the original file
    original_file_path = os.path.join('uploads', uploaded_file.filename)
    uploaded_file.save(original_file_path)

    # Process the file for transcription
    if original_file_path.lower().endswith(('.mp4', '.mov')):
        # Extract audio using FFmpeg
        subprocess.run(['ffmpeg', '-y', '-i', original_file_path, '-ac', '1', '-ar', '16000', '-vn', audio_file_path])
    elif original_file_path.lower().endswith('.wav'):
        os.rename(original_file_path, audio_file_path)
    else:
        return jsonify({'message': 'Unsupported file format'}), 400

 # Load the Whisper model and transcribe
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_file_path)
    
    # Save the transcription
    with open(transcript_file_path, 'w') as transcript_file:
        transcript_file.write(result['text'])
    
    # Save metadata
    metadata = {
        'filename': uploaded_file.filename,
        'model_size': model_size,
        'transcription_date': datetime.utcnow().isoformat()  # Add more metadata as needed
    }
    metadata_file_path = os.path.join('transcripts', filename_without_extension + '_metadata.json')
    with open(metadata_file_path, 'w') as metadata_file:
        json.dump(metadata, metadata_file, indent=4)

    return jsonify({'message': 'File uploaded and transcribed successfully', 'filename': uploaded_file.filename})

@app.route('/api/check-progress', methods=['GET'])
def check_progress():
    filename = request.args.get('filename')
    if filename:
        file_path = os.path.join('uploads', filename)
        if os.path.exists(file_path):
            current_size = os.stat(file_path).st_size
            return jsonify({"current_size": current_size})
    return jsonify({"error": "File not found"}), 404

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    # Assuming the original file is in .wav format and the transcript is in .txt format
    transcript_filename = filename
    return send_from_directory('transcripts', transcript_filename)

@app.route('/api/transcript-available/<filename>', methods=['GET'])
def transcript_available(filename):
    # Assuming the transcript file naming follows a specific pattern
    # Adjust the logic based on your actual transcript file naming convention
    transcript_filename = filename.rsplit('.', 1)[0] + '_transcribe.txt'
    transcript_path = os.path.join('transcripts', transcript_filename)
    return jsonify({"available": os.path.exists(transcript_path)})

@app.route('/api/transcript/<filename>', methods=['GET'])
def get_transcript(filename):
    transcript_filename = filename.rsplit('.', 1)[0] + '_transcribe.txt'
    transcript_path = os.path.join('transcripts', transcript_filename)
    if os.path.exists(transcript_path):
        with open(transcript_path, 'r') as file:
            transcription = file.read()
            return jsonify({"transcription": transcription})
    
    return jsonify({"error": "Transcript not found"}), 404

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9010)
