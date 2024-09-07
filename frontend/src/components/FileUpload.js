import React, { useState, useRef, useEffect } from 'react';
import { Button, Box, CircularProgress, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle } from '@mui/material';
import { CloudUpload as CloudUploadIcon, Cancel as CancelIcon } from '@mui/icons-material';  // Material UI Icons
import { toast } from 'react-toastify';
import axios from 'axios';
import API_BASE_URL from '../config';  // API base URL

const FileUpload = ({ onUploadSuccess, refresh }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);  // Single loading state to track the spinner
  const [openDialog, setOpenDialog] = useState(false);  // Track if the confirmation dialog is open
  const [dragging, setDragging] = useState(false);  // Track drag state
  const cancelTokenSource = useRef(null);  // Reference for cancel token
  const fileInputRef = useRef(null);  // Reference for the file input element

  useEffect(() => {
    if (refresh) {
      setFile(null);  // Reset file input when all files are deleted
      if (fileInputRef.current) {
        fileInputRef.current.value = '';  // Clear file input field
      }
    }
  }, [refresh]);

  // Handle file selection
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);  // Update state with selected file
    }
  };

  // Handle drag over event
  const handleDragOver = (e) => {
    e.preventDefault();
    setDragging(true);
  };

  // Handle drag leave event
  const handleDragLeave = () => {
    setDragging(false);
  };

  // Handle file drop event
  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    const droppedFile = e.dataTransfer.files[0];
    setFile(droppedFile);  // Set the dropped file to state
  };

  // Function to check if the file exists on the server
  const checkFileExists = async (filename) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/check-file/${filename}`);
      return response.data.exists;
    } catch (error) {
      console.error('Error checking file existence', error);
      return false;
    }
  };

  // Handle file upload
  const handleUpload = async () => {
    if (!file) {
      toast.error('Please select a file to upload');
      return;
    }

    // Check if the file exists on the server before uploading
    const exists = await checkFileExists(file.name);

    if (exists) {
      setOpenDialog(true);  // Open confirmation dialog if the file exists
    } else {
      // Proceed with the upload if the file does not exist
      await proceedWithUpload();
    }
  };

  // Function to proceed with the upload
  const proceedWithUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('model_size', 'base');  // Can be dynamic if needed

    try {
      setLoading(true);  // Set loading state to show spinner

      cancelTokenSource.current = axios.CancelToken.source();  // Initialize the cancel token

      const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        cancelToken: cancelTokenSource.current.token,  // Pass the cancel token to the axios request
      });

      toast.success(response.data.message);
      onUploadSuccess();  // Trigger refresh after successful upload
      setFile(null);  // Clear file input after successful upload
      if (fileInputRef.current) {
        fileInputRef.current.value = '';  // Clear the file input field in the DOM
      }
    } catch (error) {
      if (axios.isCancel(error)) {
        toast.info('Upload canceled');
      } else {
        toast.error('Error uploading file');
      }
    } finally {
      setLoading(false);  // Reset loading state
      cancelTokenSource.current = null;  // Reset cancel token
    }
  };

  // Cancel the ongoing upload
  const handleCancelUpload = () => {
    if (cancelTokenSource.current) {
      cancelTokenSource.current.cancel();  // Trigger the cancel token
      setFile(null);  // Reset the selected file
      if (fileInputRef.current) {
        fileInputRef.current.value = '';  // Clear the file input field in the DOM
      }
      setLoading(false);  // Reset loading state
    }
  };

  // Handle dialog close for confirmation
  const handleDialogClose = (confirm) => {
    setOpenDialog(false);  // Close the dialog
    if (confirm) {
      // User confirmed to overwrite the file
      proceedWithUpload();  // Proceed with upload
    } else {
      // User canceled the overwrite
      setFile(null);  // Reset the file selection
      if (fileInputRef.current) {
        fileInputRef.current.value = '';  // Clear the file input field in the DOM
      }
    }
  };

  const isUploadDisabled = loading || !file;

  return (
    <Box sx={{ p: 2, display: 'flex', alignItems: 'center', gap: 2 }}>
      {/* Drag and Drop Area */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        style={{
          border: dragging ? '2px dashed #1976d2' : '2px dashed #ccc',
          padding: '20px',
          width: '200px',
          height: '100px',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          backgroundColor: dragging ? '#f0f0f0' : 'transparent',
        }}
      >
        {file ? file.name : 'Drag & Drop File Here'}
      </div>

      {/* Hidden file input field */}
      <input
        ref={fileInputRef}  // Attach the ref to the file input field
        accept="audio/*, video/*"
        style={{ display: 'none' }}
        id="file-upload"
        type="file"
        onChange={handleFileChange}
      />
      
      {/* Custom label for the "Choose File" button */}
      <label htmlFor="file-upload">
        <Button
          variant="contained"
          color="primary"
          component="span"
          startIcon={<CloudUploadIcon />}
          sx={{
            textTransform: 'none',
            backgroundColor: '#1976d2',
            '&:hover': {
              backgroundColor: '#1565c0',
            },
          }}
        >
          {file ? file.name : 'Choose File'} {/* Display selected file name or 'Choose File' */}
        </Button>
      </label>

      {/* Upload Button */}
      <Button
        variant="contained"
        color="secondary"
        onClick={handleUpload}
        disabled={isUploadDisabled}  // Disable button during loading or if no file is selected
        startIcon={loading ? <CircularProgress size={20} /> : null}  // Show spinner during loading
        sx={{ textTransform: 'none' }}
      >
        {loading ? 'Processing...' : 'Transcribe'} {/* Change the button text */}
      </Button>

      {/* Cancel Upload Button */}
      {loading && (
        <Button
          variant="outlined"
          color="error"
          onClick={handleCancelUpload}
          startIcon={<CancelIcon />}
          sx={{ textTransform: 'none' }}
        >
          Cancel
        </Button>
      )}

      {/* Confirmation Dialog */}
      <Dialog
        open={openDialog}
        onClose={() => handleDialogClose(false)}
      >
        <DialogTitle>File Exists</DialogTitle>
        <DialogContent>
          <DialogContentText>
            A file with the name "{file?.name}" already exists. Do you want to overwrite the existing file and transcribe it again?
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => handleDialogClose(false)} color="primary">
            Cancel
          </Button>
          <Button onClick={() => handleDialogClose(true)} color="secondary">
            Overwrite
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default FileUpload;
