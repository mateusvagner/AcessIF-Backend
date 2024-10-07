from database.model.audio_transcription import AudioTranscription


class GetTranscriptionByIdUseCase:

    def execute(self, user_id: int, transcription_id: int) -> AudioTranscription:
        transcription = AudioTranscription.query.filter_by(user_id=user_id, id=transcription_id).first()
        return transcription
