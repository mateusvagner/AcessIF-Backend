from database.model.audio_transcription import AudioTranscription
from mapper.audio_transcription_mapper import whisper_transcription_to_model
from whisper_transcriber.transcriber_interface import TranscriberInterface


class TranscribeGuestUseCase:
    def __init__(self, transcriber: TranscriberInterface):
        self.transcriber = transcriber

    def execute(self, file: bytes) -> AudioTranscription:
        # Transcribe the file using the TranscriberInterface
        transcription = self.transcriber.transcribe(file)

        # Convert the transcription into an AudioTranscription model without saving
        audio_transcription = whisper_transcription_to_model(transcription, user_id=0, audio_id="",
                                                             name="Demo Transcription")
        return audio_transcription
