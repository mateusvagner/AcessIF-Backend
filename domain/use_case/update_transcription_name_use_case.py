from database.model.audio_transcription import AudioTranscription
from service.db_service import DbService


class UpdateTranscriptionNameUseCase:
    def __init__(self, db_service: DbService):
        self.db_service = db_service

    def execute(self, transcription_id: int, new_name: str) -> AudioTranscription:
        if not new_name:
            raise ValueError("Transcription name cannot be empty")

        # Update the transcription name using DbService
        updated_transcription = self.db_service.update_transcription_name(transcription_id, new_name)

        if not updated_transcription:
            raise ValueError(f"No transcription found with ID {transcription_id}")

        return updated_transcription
