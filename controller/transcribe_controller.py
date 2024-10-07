import json

from flask import Blueprint, request, jsonify

from database.model.user import User
from domain.use_case.transcribe_demo_use_case import TranscribeGuestUseCase
from domain.use_case.transcribe_use_case import TranscribeUseCase
from flask_jwt_extended import get_jwt_identity, jwt_required

from service.db_service import DbService
from service.file_service import FileService
from whisper_transcriber.transcriber import Transcriber

transcribe_bp = Blueprint('transcribe', __name__)
transcribe_use_case = TranscribeUseCase(transcriber=Transcriber(), file_service=FileService(), db_service=DbService())
transcribe_guest_use_case = TranscribeGuestUseCase(transcriber=Transcriber())


@transcribe_bp.route('/transcribe', methods=['POST'])
@jwt_required()
def transcribe_authenticated():
    file_data = request.data

    if not file_data:
        return jsonify({"error": "The file is empty"}), 400

    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    transcription = transcribe_use_case.execute(file=file_data, user=user)

    return jsonify(
        {
            'id': transcription.id,
            'audio_id': transcription.audio_id,
            'name': transcription.name,
            'text': transcription.text,
            'language': transcription.language,
            'segments': json.loads(transcription.segments),
            'created_at': transcription.created_at.isoformat() + 'Z' if transcription.created_at else None,
        }
    ), 200


@transcribe_bp.route('/transcribe/id', methods=['POST'])
@jwt_required()
def transcribe_id_authenticated():
    file_data = request.data

    if not file_data:
        return jsonify({"error": "The file is empty"}), 400

    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    transcription = transcribe_use_case.execute(file=file_data, user=user)

    return jsonify(
        {
            'id': transcription.id
        }
    ), 200


@transcribe_bp.route('/transcribe/demo', methods=['POST'])
def transcribe_guest():
    file_data = request.data

    if not file_data:
        return jsonify({"error": "The file is empty"}), 400

    transcription = transcribe_guest_use_case.execute(file=file_data)

    return jsonify(
        {
            'id': 0,
            'name': transcription.name,
            'text': transcription.text,
            'language': transcription.language,
            'segments': json.loads(transcription.segments),
        }
    ), 200
