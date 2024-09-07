import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import TranscriptionList from './components/TranscriptionList';
import TranscriptionViewer from './components/TranscriptionViewer';
import { Container, Typography } from '@mui/material';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './App.css';  // Import the CSS file

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [refresh, setRefresh] = useState(false);

  const handleUploadSuccess = () => {
    setRefresh(!refresh);  // Refresh the list when a file is uploaded
  };

  const handleFileSelect = (filename) => {
    // Toggle the transcription display: if the same file is clicked, deselect it
    if (selectedFile === filename) {
      setSelectedFile(null);  // Deselect if the same file is clicked or deleted
    } else {
      setSelectedFile(filename);  // Otherwise, select the new file
    }
  };

  return (
    <Container>
      <ToastContainer />
      {/* Header Section with Logo */}
      <header>
        <img src="/images/logo.webp" alt="Logo" />
      </header>

      {/* Description Section */}
      <div className="description-container">
        <Typography className="description-heading" gutterBottom>
          Welcome to the WhisperWave
        </Typography>
        <Typography className="description-text">
          WhisperWave allows you to upload audio and video files and get them transcribed.
          Simply choose a file, upload it, and view the transcription in the list below.
        </Typography>
      </div>

      {/* File Upload and Transcription List */}
      <FileUpload onUploadSuccess={handleUploadSuccess} />
      <TranscriptionList 
        onFileSelect={handleFileSelect} 
        refresh={refresh} 
        selectedFile={selectedFile}  // Pass the selectedFile to highlight the row
      />

      {selectedFile && <TranscriptionViewer selectedFile={selectedFile} />}
    </Container>
  );
}

export default App;
