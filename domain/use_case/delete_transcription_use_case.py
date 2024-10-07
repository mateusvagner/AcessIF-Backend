from service.db_service import DbService
from service.file_service import FileService


class DeleteTranscriptionUseCase:
    def __init__(self, db_service: DbService, file_service: FileService):
        self.db_service = db_service
        self.file_service = file_service

    def execute(self, transcription_id: int) -> None:
        if not transcription_id:
            raise ValueError("Transcription ID is required")

        # Get the transcription and delete it using DbService
        transcription = self.db_service.delete_transcription(transcription_id)

        if not transcription:
            raise ValueError(f"No transcription found with ID {transcription_id}")

        # Delete the corresponding audio file using FileService
        try:
            self.file_service.delete_file(user_id=transcription.user_id, file_id=transcription.audio_id)
        except FileNotFoundError:
            # You may log this as a warning, if the audio file is not found
            pass
