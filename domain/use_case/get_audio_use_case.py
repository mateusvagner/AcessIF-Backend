from database.model.user import User
from service.file_service import FileService


class GetAudioUseCase:

    def __init__(self, file_service: FileService):
        self.file_service = file_service

    def execute(self, user: User, audio_id: str) -> (bytes, str):
        # Use the FileService to retrieve the audio file content
        return self.file_service.get_file(user, audio_id)
