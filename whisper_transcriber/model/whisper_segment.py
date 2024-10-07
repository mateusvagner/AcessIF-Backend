from typing import List


class WhisperSegment:
    def __init__(self, segment_id: int, seek: int, start: float, end: float, text: str, tokens: List[int],
                 temperature: float, avg_logprob: float, compression_ratio: float, no_speech_prob: float):
        self.id = segment_id
        self.seek = seek
        self.start = start
        self.end = end
        self.text = text
        self.tokens = tokens
        self.temperature = temperature
        self.avg_logprob = avg_logprob
        self.compression_ratio = compression_ratio
        self.no_speech_prob = no_speech_prob

    def __repr__(self):
        return f"Segment(id={self.id}, start={self.start}, end={self.end}, text={self.text})"
