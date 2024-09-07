import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';
import { Box, IconButton, Typography } from '@mui/material';
import { ContentCopy } from '@mui/icons-material';
import API_BASE_URL from '../config';  // Import the API base URL

const TranscriptionViewer = ({ selectedFile }) => {
  const [transcription, setTranscription] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (selectedFile) {
      fetchTranscription(selectedFile);
    }
  }, [selectedFile]);

  const fetchTranscription = async (filename) => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE_URL}/transcription/${filename}`);
      setTranscription(response.data.transcription_text);
      setLoading(false);
    } catch (error) {
      toast.error('Error fetching transcription');
      setLoading(false);
    }
  };

  const handleCopyToClipboard = () => {
    if (transcription) {
      navigator.clipboard.writeText(transcription)
        .then(() => toast.success('Copied to clipboard!'))
        .catch(() => toast.error('Failed to copy!'));
    }
  };

  if (loading) {
    return <div>Loading transcription...</div>;
  }

  if (!selectedFile) {
    return <div>Select a file to view the transcription.</div>;
  }

  return (
    <Box sx={{ mt: 3 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Typography variant="h6">Transcription for: {selectedFile}</Typography>
        {/* Copy to Clipboard Button */}
        <IconButton onClick={handleCopyToClipboard}>
          <ContentCopy />
        </IconButton>
      </Box>
      {/* Transcription Box Styled as Code */}
      <Box 
        component="pre" 
        sx={{
          backgroundColor: '#f5f5f5',
          padding: '15px',
          borderRadius: '5px',
          overflowX: 'auto',
          fontFamily: 'monospace',
          maxHeight: '300px',  // Add some maximum height to prevent overflow
          whiteSpace: 'pre-wrap',
        }}
      >
        {transcription}
      </Box>
    </Box>
  );
};

export default TranscriptionViewer;
