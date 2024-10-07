from typing import List

from whisper_transcriber.model.whisper_segment import WhisperSegment


class WhisperTranscription:
    def __init__(self, text: str, segments: List[WhisperSegment], language: str):
        self.text = text
        self.segments = segments
        self.language = language

    def __repr__(self):
        return f"WhisperTranscription(language={self.language}, text={self.text[:50]}..., segments=[{len(self.segments)} segments])"
