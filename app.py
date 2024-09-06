import logging
from flask import Flask, request, jsonify, send_from_directory
import os
import whisper
from flask_cors import CORS
import subprocess
from werkzeug.utils import secure_filename
from datetime import datetime
import json

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__, static_folder='./react-frontend/build', static_url_path='/')
CORS(app)

# Ensure the uploads and transcripts directories exist
if not os.path.exists('uploads'):
    os.makedirs('uploads')
if not os.path.exists('transcripts'):
    os.makedirs('transcripts')


# List of supported file extensions by Whisper
SUPPORTED_EXTENSIONS = ('.mp3', '.wav', '.ogg', '.m4a', '.mp4', '.mov')

def is_safe_path(basedir, path, follow_symlinks=True):
    # Check if the path is safe to access
    if follow_symlinks:
        return os.path.realpath(path).startswith(basedir)
    return os.path.abspath(path).startswith(basedir)


@app.route('/api/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    try:
        filename = secure_filename(filename)
        file_path = os.path.join('uploads', filename)

        if not is_safe_path(os.path.join(app.root_path, 'uploads'), file_path):
            logging.warning(f"Invalid file path attempt: {file_path}")
            return jsonify({'message': 'Invalid file path'}), 400

        if not os.path.exists(file_path):
            logging.warning(f"File {filename} not found.")
            return jsonify({'message': 'File not found'}), 404

        os.remove(file_path)
        logging.info(f"File {filename} deleted successfully.")
        return jsonify({'message': 'File deleted successfully'}), 200

    except Exception as e:
        logging.error(f"Error deleting file {filename}: {str(e)}")
        return jsonify({'message': 'Error deleting file', 'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        uploaded_file = request.files['file']
        model_size = request.form.get('model_size', 'base')

        if not uploaded_file:
            logging.error("No file uploaded.")
            return jsonify({'message': 'No file uploaded'}), 400

        # Get the file extension and validate
        file_extension = os.path.splitext(uploaded_file.filename)[1].lower()
        if file_extension not in SUPPORTED_EXTENSIONS:
            logging.warning(f"Unsupported file format: {file_extension}")
            return jsonify({'message': 'Unsupported file format'}), 400

        # Logging the file upload start
        logging.info(f"Received file: {uploaded_file.filename}, using model size: {model_size}")

        # Remove file extension and add a new one for consistency
        filename_without_extension = os.path.splitext(uploaded_file.filename)[0]
        transcript_file_path = os.path.join('transcripts', filename_without_extension + '_transcribe.txt')

        # Save the original file
        original_file_path = os.path.join('uploads', uploaded_file.filename)
        uploaded_file.save(original_file_path)
        logging.info(f"File saved: {original_file_path}")

        # No conversion necessary for supported formats (mp4, mov, mp3, wav, etc.)
        audio_file_path = original_file_path
        logging.info(f"Processing file for transcription: {audio_file_path}")

        # Load the Whisper model and transcribe
        logging.info(f"Loading Whisper model: {model_size}")
        model = whisper.load_model(model_size)

        logging.info(f"Starting transcription for file: {audio_file_path}")
        result = model.transcribe(audio_file_path)
        logging.info(f"Transcription complete for file: {audio_file_path}")

        # Save the transcription
        with open(transcript_file_path, 'w') as transcript_file:
            transcript_file.write(result['text'])
            logging.info(f"Transcription saved: {transcript_file_path}")

        # Save metadata
        metadata = {
            'filename': uploaded_file.filename,
            'model_size': model_size,
            'transcription_date': datetime.utcnow().isoformat()  # Add more metadata as needed
        }
        metadata_file_path = os.path.join('transcripts', filename_without_extension + '_metadata.json')
        with open(metadata_file_path, 'w') as metadata_file:
            json.dump(metadata, metadata_file, indent=4)
            logging.info(f"Metadata saved: {metadata_file_path}")

        return jsonify({'message': 'File uploaded and transcribed successfully', 'filename': uploaded_file.filename}), 200

    except Exception as e:
        logging.error(f"Error during file upload or transcription: {str(e)}")
        return jsonify({'message': 'Error uploading or processing file', 'error': str(e)}), 500


@app.route('/api/files', methods=['GET'])
def list_files():
    try:
        files = os.listdir('uploads')
        logging.info(f"Listing files in uploads: {files}")
        return jsonify({"files": files}), 200
    except Exception as e:
        logging.error(f"Error listing files: {str(e)}")
        return jsonify({'message': 'Error listing files', 'error': str(e)}), 500


@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        transcript_filename = filename
        logging.info(f"Downloading transcript: {transcript_filename}")
        return send_from_directory('transcripts', transcript_filename), 200
    except Exception as e:
        logging.error(f"Error downloading transcript: {str(e)}")
        return jsonify({'message': 'Error downloading transcript', 'error': str(e)}), 500


@app.route('/api/transcript-available/<filename>', methods=['GET'])
def transcript_available(filename):
    try:
        transcript_filename = filename.rsplit('.', 1)[0] + '_transcribe.txt'
        transcript_path = os.path.join('transcripts', transcript_filename)
        available = os.path.exists(transcript_path)
        logging.info(f"Transcript availability check for {transcript_filename}: {available}")
        return jsonify({"available": available}), 200
    except Exception as e:
        logging.error(f"Error checking transcript availability for {filename}: {str(e)}")
        return jsonify({'message': 'Error checking transcript availability', 'error': str(e)}), 500


@app.route('/api/transcript/<filename>', methods=['GET'])
def get_transcript(filename):
    try:
        transcript_filename = filename.rsplit('.', 1)[0] + '_transcribe.txt'
        transcript_path = os.path.join('transcripts', transcript_filename)

        if not os.path.exists(transcript_path):
            logging.warning(f"Transcript not found for {transcript_filename}")
            return jsonify({'message': 'Transcript not found'}), 404

        with open(transcript_path, 'r') as file:
            transcription = file.read()
            logging.info(f"Serving transcript for {transcript_filename}")
            return jsonify({"transcription": transcription}), 200

    except Exception as e:
        logging.error(f"Error retrieving transcription for {filename}: {str(e)}")
        return jsonify({'message': 'Error retrieving transcription', 'error': str(e)}), 500


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        logging.info(f"Serving React frontend: index.html")
        return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9010)
