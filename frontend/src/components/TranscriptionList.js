import React, { useState, useEffect } from 'react';
import { Table, TableBody, TableCell, TableHead, TableRow, IconButton } from '@mui/material';
import { Delete } from '@mui/icons-material';
import axios from 'axios';
import { toast } from 'react-toastify';
import API_BASE_URL from '../config';  // Import the API base URL

const TranscriptionList = ({ onFileSelect, refresh, selectedFile }) => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchFiles();
  }, [refresh]);

  const fetchFiles = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE_URL}/files`);  // Use the base URL
      setFiles(response.data);
      setLoading(false);
    } catch (error) {
      toast.error('Error fetching files');
      setLoading(false);
    }
  };

  const handleDelete = async (event, filename) => {
    event.stopPropagation();  // Stop propagation to prevent triggering other click events
    try {
      await axios.delete(`${API_BASE_URL}/delete/${filename}`);  // Call the delete API
      toast.success('File deleted successfully');
  
      // Call the parent's handler to clear the selected file if needed
      if (filename === selectedFile) {
        onFileSelect(null); // Deselect the file if it's currently selected
      }
  
      // Remove the deleted file from the local state
      setFiles(files.filter(file => file.filename !== filename));
    } catch (error) {
      toast.error('Error deleting file');
    }
  };

  const handleFileClick = async (filename) => {
    onFileSelect(filename);
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();  // Format date and time
  };

  if (loading) {
    return <div>Loading files...</div>;
  }

  if (files.length === 0) {
    return <div>No files found. Please upload one.</div>;
  }

  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>File Name</TableCell>
          <TableCell>Creation Date</TableCell> {/* New Column for Creation Date */}
          <TableCell>Actions</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {files.map((file, index) => (
          <TableRow 
            key={index} 
            onClick={() => handleFileClick(file.filename)} 
            style={{
              cursor: 'pointer',
              backgroundColor: selectedFile === file.filename ? '#f0f0f0' : 'white', // Highlight selected row
            }}
          >
            <TableCell>
              {file.filename}
            </TableCell>
            <TableCell>
              {formatDate(file.upload_timestamp)} {/* Format and display creation date */}
            </TableCell>
            <TableCell>
              <IconButton 
                onClick={(event) => handleDelete(event, file.filename)}  // Pass the event to handleDelete
              >
                <Delete />
              </IconButton>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};

export default TranscriptionList;
