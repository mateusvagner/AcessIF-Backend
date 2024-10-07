from database.database import db


class Summary(db.Model):
    __tablename__ = 'summaries'

    id = db.Column(db.Integer, primary_key=True)
    transcription_id = db.Column(db.Integer, db.ForeignKey('audio_transcriptions.id'), unique=True, nullable=False)

    text = db.Column(db.Text, nullable=False)

    transcription = db.relationship('AudioTranscription', backref=db.backref('summaries', lazy=True))

    def __repr__(self):
        return f'<Summary {self.id}>'
