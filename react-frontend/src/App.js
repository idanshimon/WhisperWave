import React, { useState, useEffect } from 'react';
import FileUpload from './components/FileUpload';
import FileList from './components/FileList';
import TranscriptionViewer from './components/TranscriptionViewer';
import { Container, Row, Col } from 'reactstrap';
import axios from 'axios';

function App() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [transcription, setTranscription] = useState('');
    const [files, setFiles] = useState([]);

    // Fetch files on mount
    useEffect(() => {
        fetchFiles();
    }, []);

    const fetchFiles = async () => {
        try {
            const result = await axios.get('http://localhost:9010/api/files');
            setFiles(result.data.files);
        } catch (error) {
            console.error('Error fetching files:', error);
        }
    };

    const handleSelectFile = async (filename) => {
        setSelectedFile(filename);
        try {
            const response = await axios.get(`http://localhost:9010/api/transcript/${filename}`);
            setTranscription(response.data.transcription);
        } catch (error) {
            console.error('Failed to fetch transcription:', error);
            setTranscription("Failed to load transcription.");
        }
    };

    const handleDownloadTranscript = (filename) => {
        const transcriptFilename = filename.replace(/\.[^/.]+$/, "") + "_transcribe.txt";
        window.location.href = `http://localhost:9010/api/download/${transcriptFilename}`;
    };

    const handleDeleteFile = async (filename) => {
        if (window.confirm(`Are you sure you want to delete ${filename}?`)) {
            try {
                const response = await axios.delete(`http://localhost:9010/api/delete/${filename}`);
                alert(response.data.message);
                // Re-fetch the file list after deletion
                const updatedFiles = await axios.get('http://localhost:9010/api/files');
                setFiles(files.filter(file => file !== filename));
            } catch (error) {
                console.error('Error deleting file:', error);
                alert('Error deleting file.');
            }
        }
    };

    return (
        <Container fluid className="mt-4">
            <Row>
                <Col md={4}>
                    <FileUpload onUploadSuccess={fetchFiles} />
                </Col>
                <Col md={8}>
                    <TranscriptionViewer selectedFile={selectedFile} transcription={transcription} />
                </Col>
            </Row>
            <Row>
                <Col md={12}>
                    <FileList 
                        files={files}
                        onSelectFile={handleSelectFile}
                        onDownloadTranscript={handleDownloadTranscript}
                        onDeleteFile={handleDeleteFile}
                    />
                </Col>
            </Row>
        </Container>
    );
}

export default App;
