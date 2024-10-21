import whisper

from whisper_transcriber.file_handler import FileHandler
from mapper.whisper_transcription_mapper import whisper_dict_to_whisper_transcription
from whisper_transcriber.model.whisper_transcription import WhisperTranscription
from whisper_transcriber.transcriber_interface import TranscriberInterface


class Transcriber(TranscriberInterface):
    def transcribe(self, file: bytes) -> WhisperTranscription:
        file_handler = FileHandler(file=file)

        model = whisper.load_model('base')
        result = model.transcribe(file_handler.temp_file_path)

        file_handler.remove_temp_file()

        whisper_transcription = whisper_dict_to_whisper_transcription(result)

        return whisper_transcription
