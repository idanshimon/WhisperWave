# WhisperWave: Flask Transcription Service

WhisperWave is a transcription system that allows users to upload audio or video files for transcription using OpenAI's Whisper model. The system is built with a Flask backend and a React frontend, and supports file management functionalities such as file upload, delete, and transcription viewing.

## **Features**
- Upload audio/video files for transcription.
- Real-time transcription using the Whisper model.
- Manage uploaded files (delete, view transcripts).
- Responsive frontend built with React.
- Dockerized for ease of deployment in production.

The app can be run in both standalone mode (without containers) or using Docker containers.

### **Prerequisites**
- **Python 3.10** or higher
- **Node.js 18.x** or higher
- **npm** (comes with Node.js)
- **FFmpeg** (for handling audio and video)
- **Docker** and **Docker Compose** (for running in containers)

## **1. Running Without Containers (Standalone Mode)**
This mode is ideal for local development.

### **Backend Setup (Flask)**
1. Clone the repository:
   ```bash
   git clone https://github.com/idanshimon/WhisperWave.git
   cd WhisperWave/backend
   ```
2. Create and activate a Python virtual environment:
   ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    # or
    .\venv\Scripts\activate   # On Windows
   ```

3. Install the dependencies (including Whisper):
    ```bash
    pip install -r requirements.txt
    ```

4. Ensure FFmpeg is installed on your system:
  On macOS:
    ```bash
    brew install ffmpeg
    ```
    On Ubuntu/Debian:
    ```bash
    sudo apt update && sudo apt install ffmpeg
    ```
5. Run the Flask app:
    ```bash
    python app.py
    ```
The Flask backend will start on http://localhost:9010.

## Frontend Setup (React)
1. In a new terminal, navigate to the frontend directory:
    ```bash
    cd WhisperWave/frontend
    ```
2. Install the frontend dependencies and start:
   ```bash
   npm install
    ```
3. Start the React development server:
    ```bash
    npm start
    ```
The frontend will run on http://localhost:3000, and it will proxy API requests to the Flask backend on port 9010.

## **2. Running with Docker Containers **
This mode is ideal for production or containerized environments.

### Setup Using Docker Compose
Docker Compose will build and run both the backend (Flask) and the frontend (React) as separate services.

1. Clone the repository:
   ```bash
   git clone https://github.com/idanshimon/WhisperWave.git
   cd WhisperWave/backend
   ```
2. Build and run the app using Docker Compose:

    ```bash
    docker-compose up --build
    ```

This will:

* Build the backend (Flask) container and expose it on port 9010.
* Build the frontend (React) container and serve it via Nginx on port 3000.

### Stopping the Containers
To stop the running containers:
```bash
docker-compose down
```

# License
This project is licensed under the MIT License. See the LICENSE file for details.


# Author
Idan Shimon