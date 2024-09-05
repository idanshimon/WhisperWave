import React from 'react';
import { Card, CardBody, CardTitle, CardText } from 'reactstrap';

const TranscriptionViewer = ({ selectedFile, transcription }) => {
    if (!selectedFile) {
        return <div>Select a file to view its transcription.</div>;
    }

    return (
        <Card>
            <CardBody>
                <CardTitle tag="h5">Transcription: {selectedFile}</CardTitle>
                <CardText>
                    {transcription || "Select a file to view its transcription."}
                </CardText>
            </CardBody>
        </Card>
    );
};

export default TranscriptionViewer;