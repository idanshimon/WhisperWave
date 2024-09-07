import os
import shutil
import tarfile
from datetime import datetime

# Paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'database.db')
UPLOADS_PATH = os.path.join(BASE_DIR, 'uploads')
TRANSCRIPTS_PATH = os.path.join(BASE_DIR, 'transcripts')
BACKUP_DIR = os.path.join(BASE_DIR, 'backups')

# Ensure backup directory exists
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

def backup():
    """
    Backs up the SQLite database, uploads, and transcripts directories to a single tar file in the 'backups' directory.
    """
    try:
        # Ensure the critical directories exist
        if not os.path.exists(DATABASE_PATH):
            raise Exception("Database file not found!")
        if not os.path.exists(UPLOADS_PATH):
            raise Exception("Uploads directory not found!")
        if not os.path.exists(TRANSCRIPTS_PATH):
            raise Exception("Transcripts directory not found!")

        # Create a timestamped tar file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(BACKUP_DIR, f'backup_{timestamp}.tar.gz')

        with tarfile.open(backup_file, "w:gz") as tar:
            # Add the SQLite database to the archive
            tar.add(DATABASE_PATH, arcname=os.path.basename(DATABASE_PATH))
            print(f"Added database to backup: {DATABASE_PATH}")

            # Add the uploads directory to the archive
            tar.add(UPLOADS_PATH, arcname='uploads')
            print(f"Added uploads to backup: {UPLOADS_PATH}")

            # Add the transcripts directory to the archive
            tar.add(TRANSCRIPTS_PATH, arcname='transcripts')
            print(f"Added transcripts to backup: {TRANSCRIPTS_PATH}")

        print(f"Backup completed successfully to {backup_file}")
    except Exception as e:
        print(f"Error during backup: {e}")

def restore(backup_file):
    """
    Restores the SQLite database, uploads, and transcripts directories from the specified tar file.
    """
    try:
        # Ensure the backup file exists
        if not os.path.exists(backup_file):
            raise Exception(f"Backup file '{backup_file}' does not exist.")

        with tarfile.open(backup_file, "r:gz") as tar:
            # Extract the SQLite database
            tar.extract('database.db', path=BASE_DIR)
            print(f"Database restored from backup: {DATABASE_PATH}")

            # Extract the uploads directory directly to its correct location
            uploads_backup_path = os.path.join(BASE_DIR, 'uploads')
            if os.path.exists(UPLOADS_PATH):
                shutil.rmtree(UPLOADS_PATH)  # Remove the current uploads directory
            os.makedirs(UPLOADS_PATH)  # Recreate the uploads directory
            tar.extractall(path=BASE_DIR, members=[m for m in tar.getmembers() if m.name.startswith('uploads')])
            print(f"Uploads directory restored from backup")

            # Extract the transcripts directory directly to its correct location
            transcripts_backup_path = os.path.join(BASE_DIR, 'transcripts')
            if os.path.exists(TRANSCRIPTS_PATH):
                shutil.rmtree(TRANSCRIPTS_PATH)  # Remove the current transcripts directory
            os.makedirs(TRANSCRIPTS_PATH)  # Recreate the transcripts directory
            tar.extractall(path=BASE_DIR, members=[m for m in tar.getmembers() if m.name.startswith('transcripts')])
            print(f"Transcripts directory restored from backup")

        print("Restore completed successfully.")
    except Exception as e:
        print(f"Error during restore: {e}")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Backup and restore database, uploads, and transcripts to/from a single tar file.")
    parser.add_argument('action', choices=['backup', 'restore'], help="Choose whether to backup or restore.")
    parser.add_argument('--file', help="Specify the backup file to restore from (required for restore).")

    args = parser.parse_args()

    if args.action == 'backup':
        backup()
    elif args.action == 'restore':
        if not args.file:
            print("Please specify the backup file to restore from using the --file argument.")
        else:
            restore(args.file)
