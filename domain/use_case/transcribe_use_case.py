from database.model.user import User
from database.model.audio_transcription import AudioTranscription
from service.db_service import DbService
from service.file_service import FileService
from mapper.audio_transcription_mapper import whisper_transcription_to_model
from whisper_transcriber.transcriber_interface import TranscriberInterface


class TranscribeUseCase:
    def __init__(self, transcriber: TranscriberInterface, file_service: FileService, db_service: DbService):
        self.transcriber = transcriber
        self.file_service = file_service
        self.db_service = db_service

    def execute(self, file: bytes, user: User) -> AudioTranscription:
        transcription = self.transcriber.transcribe(file)
        # Save the audio file using the FileService and get the generated audio ID
        audio_id = self.file_service.save_file(file, user.id)

        # Use the generated audio ID for further processing (e.g., saving the transcription)
        audio_transcription = whisper_transcription_to_model(transcription=transcription, user_id=user.id,
                                                             audio_id=audio_id, name=audio_id)

        self.db_service.save_transcription(audio_transcription=audio_transcription)

        return audio_transcription
