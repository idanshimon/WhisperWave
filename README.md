# WhisperWave: Flask Transcription Service

WhisperWave is a versatile Flask application designed for efficient audio and video file transcription. Leveraging the Whisper model for accurate transcription and FFmpeg for audio extraction, WhisperWave enables users to upload, process, and manage media files seamlessly. It offers robust features including:

File Upload and Processing: Easily upload audio or video files for transcription.
Transcription Management: Retrieve, download, and check the availability of transcriptions.
File Management: List, delete, and monitor the progress of uploaded files.
Static File Serving: Serve a React-based frontend for a smooth user experience.
With WhisperWave, transform your media files into readable text quickly and effectively.

## Features

- **File Upload**: Upload audio or video files for transcription.
- **File Deletion**: Delete uploaded files.
- **File Listing**: List all uploaded files.
- **Progress Check**: Check the upload progress of a file.
- **Transcript Availability**: Check if a transcript is available for a given file.
- **Transcript Retrieval**: Get the transcript of a file.
- **Static File Serving**: Serve static files from a React frontend.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/your-repository.git
    cd your-repository
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Install FFmpeg:**

    Follow the [installation instructions](https://ffmpeg.org/download.html) for FFmpeg suitable for your operating system.
  

5. **Setup React Frontend**

    Navigate to the React frontend directory:
    ```bash
    cd react-frontend
    # Install Node.js dependencies:
    npm install
    # Test Start the React development server:
    npm start
    # The React frontend will be available at http://localhost:3000.
    ```

    
## Configuration

1. **Ensure the following directories exist:**

    - `uploads` - For storing uploaded files.
    - `transcripts` - For storing transcription files.

   These directories will be created automatically if they do not exist.

2. **Configure Whisper Model:**

    The Whisper model will be loaded based on the `model_size` parameter in the upload request. Ensure the Whisper model is available and compatible with your setup.

## Running the Application

To start the Flask server, run:

```bash
python app.py
```
The application will be accessible at http://localhost:9010.


## API Endpoints

- **`POST /api/upload`**
  
  Uploads a file for transcription. The request should include a file and an optional `model_size` parameter.
  
  **Request:**
  - **Form-data:**
    - `file`: The audio or video file to upload.
    - `model_size` (optional): The size of the Whisper model to use (e.g., `base`, `large`).
  
  **Response:**
  - `200 OK` if the file is uploaded and transcribed successfully.
  - `400 Bad Request` if the file format is unsupported.
  - `500 Internal Server Error` if an error occurs during file processing.

- **`DELETE /api/delete/<filename>`**
  
  Deletes the specified file from the `uploads` directory.
  
  **Request:**
  - **Path Parameter:**
    - `filename`: The name of the file to delete.
  
  **Response:**
  - `200 OK` if the file is deleted successfully.
  - `400 Bad Request` if the file path is invalid.
  - `404 Not Found` if the file does not exist.
  - `500 Internal Server Error` if an error occurs during deletion.

- **`GET /api/files`**
  
  Lists all files in the `uploads` directory.
  
  **Response:**
  - `200 OK` with a JSON object containing a list of filenames.

- **`GET /api/check-progress`**
  
  Checks the upload progress of a file by returning its current size.
  
  **Request:**
  - **Query Parameter:**
    - `filename`: The name of the file to check.
  
  **Response:**
  - `200 OK` with a JSON object containing the current file size.
  - `404 Not Found` if the file does not exist.

- **`GET /api/download/<filename>`**
  
  Downloads the transcript of the specified file.
  
  **Request:**
  - **Path Parameter:**
    - `filename`: The name of the transcript file to download.
  
  **Response:**
  - `200 OK` with the transcript file if it exists.
  - `404 Not Found` if the transcript file does not exist.

- **`GET /api/transcript-available/<filename>`**
  
  Checks if a transcript is available for the specified file.
  
  **Request:**
  - **Path Parameter:**
    - `filename`: The name of the file to check for a transcript.
  
  **Response:**
  - `200 OK` with a JSON object indicating whether the transcript is available (`{"available": true/false}`).

- **`GET /api/transcript/<filename>`**
  
  Retrieves the transcript of the specified file.
  
  **Request:**
  - **Path Parameter:**
    - `filename`: The name of the file for which to retrieve the transcript.
  
  **Response:**
  - `200 OK` with a JSON object containing the transcript text.
  - `404 Not Found` if the transcript file does not exist.

# Frontend
The application serves a React frontend located in the react-frontend/build directory. Make sure to build the React frontend before running the Flask application.

# License
This project is licensed under the MIT License. See the LICENSE file for details.


# Author
Idan Shimon