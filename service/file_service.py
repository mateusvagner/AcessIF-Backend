import os
from datetime import datetime
from io import BytesIO
from uuid import uuid4

from pydub import AudioSegment

from database.model.user import User

# Base directory where all user folders will be stored
AUDIO_STORAGE_BASE_PATH = "file/audio_files"

# Ensure the base directory exists
if not os.path.exists(AUDIO_STORAGE_BASE_PATH):
    os.makedirs(AUDIO_STORAGE_BASE_PATH)


class FileService:
    def __init__(self, base_path: str = AUDIO_STORAGE_BASE_PATH):
        self.base_path = base_path
        # Ensure the base directory exists
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def save_file(self, file: bytes, user_id: int) -> str:
        audio_segment = AudioSegment.from_file(BytesIO(file))

        # Create a directory for the user if it doesn't exist
        user_folder = os.path.join(self.base_path, str(user_id))
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)

        # Generate the current date in YYYYMMDD format
        current_date = datetime.utcnow().strftime("%Y%m%d")

        # Generate a short unique ID (first 8 characters of a UUID)
        unique_id = str(uuid4()).split("-")[0]

        # Combine date and unique ID to form the filename
        unique_filename = f"{current_date}_{unique_id}.mp3"
        file_path = os.path.join(user_folder, unique_filename)

        # Save the file to the filesystem
        audio_segment.export(file_path, format="mp3")

        # Return the generated unique filename (acting as the audio ID)
        return unique_filename

    def get_file(self, user: User, file_id: str) -> (bytes, str):
        # Construct the file path based on user ID and file ID
        user_folder = os.path.join(self.base_path, str(user.id))
        file_path = os.path.join(user_folder, file_id)

        # Check if the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_id} for user {user.name} not found.")

        # Read the file's binary content
        with open(file_path, "rb") as f:
            file_content = f.read()

        # Return both the file content and its format
        # TODO check way to detect a file format
        return file_content, "mp3"

    def delete_file(self, user_id: int, file_id: str) -> None:
        # Construct the file path based on user ID and file ID
        user_folder = os.path.join(self.base_path, str(user_id))
        file_path = os.path.join(user_folder, file_id)

        # Check if the file exists and delete it
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            raise FileNotFoundError(f"File {file_id} for user {user_id} not found.")


