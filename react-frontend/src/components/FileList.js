import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { ListGroup, ListGroupItem, Button } from 'reactstrap';

const FileList = ({ onSelectFile, onDownloadTranscript }) => {
    const [files, setFiles] = useState([]);

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

    const handleDeleteFile = async (filename) => {
        if (window.confirm(`Are you sure you want to delete ${filename}?`)) {
            try {
                const response = await axios.delete(`http://localhost:9010/api/delete/${filename}`);
                alert(response.data.message);
                // Refresh the file list after deletion
                fetchFiles();
            } catch (error) {
                console.error('Error deleting file:', error);
                alert('Error deleting file');
            }
        }
    };

    return (
        <ListGroup>
            {files.map((file, index) => (
                <ListGroupItem key={index} className="d-flex justify-content-between align-items-center">
                    {file}
                    <div>
                        <Button color="info" onClick={() => onSelectFile(file)}>View Transcription</Button>
                        {' '}
                        <Button color="secondary" onClick={() => onDownloadTranscript(file)}>Download</Button>
                        {' '}
                        <Button color="danger" onClick={() => handleDeleteFile(file)}>Delete</Button>
                    </div>
                </ListGroupItem>
            ))}
        </ListGroup>
    );
};

export default FileList;
