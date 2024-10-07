import json

from database.model.audio_transcription import AudioTranscription
from whisper_transcriber.model.whisper_transcription import WhisperTranscription


def whisper_transcription_to_model(
        transcription: WhisperTranscription,
        user_id: int, audio_id: str, name: str) -> AudioTranscription:

    segments = [
        {"id": segment.id, "start": segment.start, "end": segment.end, "text": segment.text}
        for segment in transcription.segments
    ]
    return AudioTranscription(
        user_id=user_id,
        audio_id=audio_id,
        text=transcription.text,
        segments=json.dumps(segments),  # Convert segments list to JSON string
        language=transcription.language,
        name=name
    )
