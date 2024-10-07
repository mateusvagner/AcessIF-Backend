from abc import ABC, abstractmethod

from whisper_transcriber.model.whisper_transcription import WhisperTranscription


class TranscriberInterface(ABC):
    @abstractmethod
    def transcribe(self, file: bytes) -> WhisperTranscription:
        """Get audio or movie file and return its transcription"""
        pass
