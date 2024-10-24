from database.model.audio_transcription import AudioTranscription
from service.db_service import DbService


class FavoriteTranscriptionUseCase:
    def __init__(self, db_service: DbService):
        self.db_service = db_service

    def execute(self, transcription_id: int) -> AudioTranscription:
        if not transcription_id:
            raise ValueError("Transcription ID is required")

        # Get the transcription from DbService
        transcription = self.db_service.get_transcription(transcription_id)

        if not transcription:
            raise ValueError(f"No transcription found with ID {transcription_id}")

        # Update the 'is_favorite' property of the transcription to inverse
        transcription.is_favorite = not transcription.is_favorite

        # Save the updated transcription back to the database
        updated_transcription = self.db_service.update_transcription(transcription)

        return updated_transcription
