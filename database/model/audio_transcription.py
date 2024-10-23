from datetime import datetime
from database.database import db


class AudioTranscription(db.Model):
    __tablename__ = 'audio_transcriptions'

    id = db.Column(db.Integer, primary_key=True)

    audio_id = db.Column(db.String(36))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    name = db.Column(db.String(255), nullable=False)

    text = db.Column(db.Text, nullable=False)

    segments = db.Column(db.Text, nullable=False)  # Store segments as JSON

    language = db.Column(db.String(50), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    summary = db.relationship('Summary', uselist=False, back_populates='transcription',
                              cascade="all, delete",
                              overlaps="summaries")

    is_favorite = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<AudioTranscription {self.id} for AudioFile {self.audio_id}>'
