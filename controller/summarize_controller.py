from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from database.model.audio_transcription import AudioTranscription
from domain.use_case.summarize_use_case import SummarizeUseCase
from llm_summarizer.summarizer import Summarizer
from service.db_service import DbService

summarize_bp = Blueprint('summarize', __name__)

summarize_use_case = SummarizeUseCase(llm_summarizer=Summarizer(), db_service=DbService())


@summarize_bp.route('/summarize/<int:transcription_id>', methods=['GET'])
@jwt_required()
def summarize(transcription_id):
    audio_transcription = AudioTranscription.query.filter_by(id=transcription_id).first()

    if not audio_transcription:
        return jsonify({'message': 'Audio transcription not found'}), 404

    summary = summarize_use_case.execute(audio_transcription)

    return jsonify(
        {
            'id': summary.id,
            'transcription_id': summary.transcription_id,
            'text': summary.text
        }
    ), 200
