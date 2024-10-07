from typing import List

from database.model.audio_transcription import AudioTranscription


class GetAllTranscriptionsUseCase:

    def execute(self, user_id: int, limit: int = None) -> List[AudioTranscription]:
        query = AudioTranscription.query.filter_by(user_id=user_id).order_by(AudioTranscription.created_at.desc())
        if limit:
            query = query.limit(limit)
        return query.all()
