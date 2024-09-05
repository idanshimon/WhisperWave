FROM python:3.11
RUN apt-get update && apt-get install -y ffmpeg git
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip

# Install Python dependencies
COPY requirements.txt .
RUN pip install flask
RUN pip install git+https://github.com/openai/whisper.git 

# Expose the port the app runs on
EXPOSE 9010

# Create a volume for uploads
VOLUME ["/app/uploads"]

# Command to run the application
CMD ["python", "app.py"]
