import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os
import whisper
from werkzeug.utils import secure_filename  # Import secure_filename
from datetime import datetime

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__, static_folder='../frontend/build', static_url_path='')
CORS(app, resources={r"/api/*": {"origins": "*"}})


# Serve React App
@app.route('/')
def serve():
    logging.info("Serving React frontend.")
    return send_from_directory(app.static_folder, 'index.html')

# Add additional routes to handle any frontend requests
@app.errorhandler(404)
def not_found(e):
    logging.warning("404 error encountered. Serving React frontend for route.")
    return send_from_directory(app.static_folder, 'index.html')


# SQLite database setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

UPLOAD_FOLDER = 'uploads'
TRANSCRIPTS_FOLDER = 'transcripts'

# Ensure upload and transcript directories exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    logging.info(f"Created upload directory at {UPLOAD_FOLDER}")

if not os.path.exists(TRANSCRIPTS_FOLDER):
    os.makedirs(TRANSCRIPTS_FOLDER)
    logging.info(f"Created transcripts directory at {TRANSCRIPTS_FOLDER}")

# File metadata model
class FileMetadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    file_type = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='pending')
    upload_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    transcription_text = db.Column(db.Text, nullable=True)

# Upload file endpoint
@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'message': 'No file provided'}), 400

        file = request.files['file']
        filename = secure_filename(file.filename)  # Secure the filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        # Overwrite the existing file if it already exists
        if os.path.exists(file_path):
            logging.info(f"Overwriting file {filename}")

        # Save the file (overwrite if exists)
        file.save(file_path)
        logging.info(f"File saved: {file_path}")

        # Check if file metadata already exists in the database
        file_metadata = FileMetadata.query.filter_by(filename=filename).first()

        if file_metadata:
            # If file exists, update the metadata
            logging.info(f"File {filename} already exists in the database, updating entry.")
            file_metadata.upload_timestamp = datetime.utcnow()
            file_metadata.status = 'pending'
        else:
            # If file does not exist, create new metadata
            file_metadata = FileMetadata(
                filename=filename,
                file_type=filename.split('.')[-1],
                status='pending'
            )
            db.session.add(file_metadata)

        db.session.commit()

        # Transcribe the file using Whisper
        logging.info(f"Starting transcription for {filename}")
        model = whisper.load_model('base')
        result = model.transcribe(file_path)
        transcription_path = os.path.join(TRANSCRIPTS_FOLDER, f'{os.path.splitext(filename)[0]}.txt')

        with open(transcription_path, 'w') as f:
            f.write(result['text'])
        logging.info(f"Transcription complete for {filename}. Saved to {transcription_path}")

        # Update the metadata after transcription
        file_metadata.status = 'completed'
        file_metadata.transcription_text = result['text']
        db.session.commit()

        return jsonify({'message': 'File uploaded and transcribed successfully'}), 200

    except Exception as e:
        logging.error(f"Error during file upload or transcription: {str(e)}")
        return jsonify({'message': 'Error during upload or transcription', 'error': str(e)}), 500



# Endpoint to list files
@app.route('/api/files', methods=['GET'])
def list_files():
    logging.info("Fetching list of files.")
    files = FileMetadata.query.all()
    
    if not files:
        logging.info("No files found.")
        return jsonify([]), 200  # Return an empty list if no files
    
    return jsonify([{
        'filename': file.filename,
        'status': file.status,
        'transcription_text': file.transcription_text,
        'upload_timestamp': file.upload_timestamp
    } for file in files]), 200


# Check if a file with the same name exists
@app.route('/api/check-file/<filename>', methods=['GET'])
def check_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return jsonify({'exists': True}), 200
    return jsonify({'exists': False}), 200

# Endpoint to serve uploaded files
@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    logging.info(f"Downloading file {filename}")
    return send_from_directory(UPLOAD_FOLDER, filename)

# Endpoint to retrieve transcription
@app.route('/api/transcription/<filename>', methods=['GET'])
def get_transcription(filename):
    logging.info(f"Retrieving transcription for {filename}")
    file_metadata = FileMetadata.query.filter_by(filename=filename).first()
    if not file_metadata:
        logging.error(f"File {filename} not found.")
        return jsonify({'message': 'File not found'}), 404
    return jsonify({'transcription_text': file_metadata.transcription_text})

# Endpoint to delete files
@app.route('/api/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    logging.info(f"Deleting file {filename}")
    file_metadata = FileMetadata.query.filter_by(filename=filename).first()
    if not file_metadata:
        logging.error(f"File {filename} not found.")
        return jsonify({'message': 'File not found'}), 404

    # Delete files from uploads and transcripts
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    transcript_path = os.path.join(TRANSCRIPTS_FOLDER, f'{os.path.splitext(filename)[0]}.txt')

    if os.path.exists(file_path):
        os.remove(file_path)
        logging.info(f"Deleted file {file_path}")
    if os.path.exists(transcript_path):
        os.remove(transcript_path)
        logging.info(f"Deleted transcription file {transcript_path}")

    db.session.delete(file_metadata)
    db.session.commit()

    return jsonify({'message': 'File deleted successfully'}), 200

if __name__ == '__main__':
    logging.info("Starting Flask app.")
    app.run(debug=True, host='0.0.0.0', port=9010)
