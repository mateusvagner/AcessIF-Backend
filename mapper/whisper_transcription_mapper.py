from whisper_transcriber.model.whisper_segment import WhisperSegment
from whisper_transcriber.model.whisper_transcription import WhisperTranscription


def whisper_dict_to_whisper_transcription(data) -> WhisperTranscription:
    segments = [WhisperSegment(
        segment_id=seg['id'],
        seek=seg['seek'],
        start=seg['start'],
        end=seg['end'],
        text=seg['text'],
        tokens=seg['tokens'],
        temperature=seg['temperature'],
        avg_logprob=seg['avg_logprob'],
        compression_ratio=seg['compression_ratio'],
        no_speech_prob=seg['no_speech_prob']
    ) for seg in data['segments']]

    return WhisperTranscription(
        text=data['text'],
        segments=segments,
        language=data['language']
    )
