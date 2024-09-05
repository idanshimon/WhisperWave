#!/bin/bash

# Define variables
BACKUP_FILE="transcripts.tar.gz"
TRANSCRIPTS_DIR="transcripts"

# Function to compress the transcripts directory
compress_transcripts() {
    echo "Compressing the '$TRANSCRIPTS_DIR' directory into '$BACKUP_FILE'..."
    tar -czvf "$BACKUP_FILE" "$TRANSCRIPTS_DIR"
    echo "Compression complete."
}

# Function to decompress the backup file
decompress_transcripts() {
    echo "Decompressing '$BACKUP_FILE'..."
    tar -xzvf "$BACKUP_FILE"
    echo "Decompression complete."
}

# Check the command-line argument and execute the appropriate function
if [ "$1" == "compress" ]; then
    compress_transcripts
elif [ "$1" == "decompress" ]; then
    decompress_transcripts
else
    echo "Usage: $0 {compress|decompress}"
    exit 1
fi
