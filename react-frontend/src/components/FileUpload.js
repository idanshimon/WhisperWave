import React, { useState } from 'react';
import axios from 'axios';
import ProgressBar from 'react-bootstrap/ProgressBar';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Button, Form, FormGroup, Label, Input, Container, Row, Col } from 'reactstrap';

const FileUpload = ({ onUploadSuccess }) => {
    const [file, setFile] = useState(null);
    const [modelSize, setModelSize] = useState('base');
    const [uploadProgress, setUploadProgress] = useState(0);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
        setUploadProgress(0); // Reset progress on new file selection
    };

    const handleModelChange = (e) => setModelSize(e.target.value);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) {
            alert("Please select a file first!");
            return;
        }

        const formData = new FormData();
        formData.append('file', file);
        formData.append('model_size', modelSize);

        try {
            await axios.post('http://localhost:9010/api/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
                onUploadProgress: progressEvent => {
                    const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                    setUploadProgress(percentCompleted);
                }
            });

            onUploadSuccess();
            alert('File uploaded and transcription started.');
        } catch (error) {
            console.error('Error uploading file:', error);
            alert('Error uploading file.');
        }
    };

    return (
        <Container className="mt-5">
            <Row>
                <Col md={{ size: 6, offset: 3 }}>
                    <Form onSubmit={handleSubmit}>
                        <FormGroup>
                            <Label for="fileUpload">Upload File</Label>
                            <Input type="file" name="file" id="fileUpload" onChange={handleFileChange} />
                        </FormGroup>
                        <FormGroup>
                            <Label for="modelSize">Model Size</Label>
                            <Input type="select" name="select" id="modelSize" onChange={handleModelChange}>
                                <option value="base">Base</option>
                                <option value="tiny">Tiny</option>
                                <option value="small">Small</option>
                                <option value="medium">Medium</option>
                                <option value="large">Large</option>
                            </Input>
                        </FormGroup>
                        <Button color="primary">Upload and Transcribe</Button>
                    </Form>
                    {uploadProgress > 0 && (
                        <ProgressBar now={uploadProgress} label={`${uploadProgress}%`} className="mt-3" />
                    )}
                </Col>
            </Row>
        </Container>
    );
};

export default FileUpload;