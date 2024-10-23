from database.database import db
from database.model.audio_transcription import AudioTranscription
from database.model.summary import Summary


class DbService:
    def __init__(self):
        pass

    def save_transcription(self, audio_transcription: AudioTranscription) -> AudioTranscription:
        db.session.add(audio_transcription)
        db.session.commit()

        return audio_transcription

    def save_summary(self, summary: Summary) -> Summary:
        db.session.add(summary)
        db.session.commit()

        return summary

    def update_transcription_name(self, transcription_id: int, new_name: str) -> AudioTranscription:
        # Find the transcription by ID
        transcription = AudioTranscription.query.get(transcription_id)

        if transcription:
            # Update the name
            transcription.name = new_name
            db.session.commit()

        return transcription

    def delete_transcription(self, transcription_id: int) -> AudioTranscription:
        # Find the transcription by ID
        transcription = AudioTranscription.query.get(transcription_id)

        if transcription:
            # Delete the transcription from the database
            db.session.delete(transcription)
            db.session.commit()
            return transcription

        return None

    def get_transcription(self, transcription_id) -> AudioTranscription:
        return AudioTranscription.query.get(transcription_id)

    def update_transcription(self, transcription) -> AudioTranscription:
        db.session.add(transcription)
        db.session.commit()
        return transcription
