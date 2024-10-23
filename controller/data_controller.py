import json
from io import BytesIO

from flask import Blueprint, jsonify, send_file, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from database.model.user import User
from domain.use_case.delete_transcription_use_case import DeleteTranscriptionUseCase
from domain.use_case.favorite_transcription_use_case import FavoriteTranscriptionUseCase
from domain.use_case.get_all_transcriptions_use_case import GetAllTranscriptionsUseCase
from domain.use_case.get_audio_use_case import GetAudioUseCase
from domain.use_case.get_transcription_by_id_use_case import GetTranscriptionByIdUseCase
from domain.use_case.update_transcription_name_use_case import UpdateTranscriptionNameUseCase
from service.db_service import DbService
from service.file_service import FileService

data_bp = Blueprint('data', __name__)

get_all_transcriptions_use_case = GetAllTranscriptionsUseCase()
get_transcriptions_by_id_use_case = GetTranscriptionByIdUseCase()
update_transcription_name_use_case = UpdateTranscriptionNameUseCase(db_service=DbService())
get_audio_use_case = GetAudioUseCase(file_service=FileService())
delete_transcription_use_case = DeleteTranscriptionUseCase(db_service=DbService(), file_service=FileService())
favorite_transcription_use_case = FavoriteTranscriptionUseCase(db_service=DbService())


@data_bp.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    current_user_email = get_jwt_identity()
    user: User = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify(
        {
            'id': user.id,
            'name': user.name,
            'email': user.email,
        }
    ), 200


@data_bp.route('/transcriptions', methods=['GET'])
@jwt_required()
def get_all_transcriptions():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    transcriptions = get_all_transcriptions_use_case.execute(user_id=user.id)

    response_data = [
        {
            'id': transcription.id,
            'audio_id': transcription.audio_id,
            'name': transcription.name,
            'text': transcription.text,
            'language': transcription.language,
            'segments': json.loads(transcription.segments),
            'created_at': transcription.created_at.isoformat() + 'Z' if transcription.created_at else None,
            'isFavorite': transcription.isFavorite,
            'summary': {
                'transcription_id': transcription.summary.transcription_id,
                'id': transcription.summary.id,
                'text': transcription.summary.text
            } if transcription.summary else None
        } for transcription in transcriptions
    ]

    return jsonify(response_data), 200


@data_bp.route('/last-transcriptions', methods=['GET'])
@jwt_required()
def get_last_transcriptions():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    transcriptions = get_all_transcriptions_use_case.execute(user_id=user.id, limit=3)

    response_data = [
        {
            'id': transcription.id,
            'audio_id': transcription.audio_id,
            'name': transcription.name,
            'text': transcription.text,
            'language': transcription.language,
            'segments': json.loads(transcription.segments),
            'created_at': transcription.created_at.isoformat() + 'Z' if transcription.created_at else None,
            'isFavorite': transcription.isFavorite,
            'summary': {
                'transcription_id': transcription.summary.transcription_id,
                'id': transcription.summary.id,
                'text': transcription.summary.text
            } if transcription.summary else None
        } for transcription in transcriptions
    ]

    return jsonify(response_data), 200


@data_bp.route('/transcriptions/<transcription_id>', methods=['GET'])
@jwt_required()
def get_transcriptions_by_id(transcription_id):
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    transcription = get_transcriptions_by_id_use_case.execute(user_id=user.id, transcription_id=transcription_id)

    return jsonify(
        {
            'id': transcription.id,
            'audio_id': transcription.audio_id,
            'name': transcription.name,
            'text': transcription.text,
            'language': transcription.language,
            'segments': json.loads(transcription.segments),
            'created_at': transcription.created_at.isoformat() + 'Z' if transcription.created_at else None,
            'isFavorite': transcription.isFavorite,
            'summary': {
                'transcription_id': transcription.summary.transcription_id,
                'id': transcription.summary.id,
                'text': transcription.summary.text
            } if transcription.summary else None
        }
    ), 200


@data_bp.route('/transcriptions/<int:transcription_id>/name', methods=['PUT'])
@jwt_required()
def update_transcription_name(transcription_id):
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    # Parse the request data
    data = request.json
    new_name = data.get('name')

    if not new_name:
        return jsonify({"message": "New transcription name is required"}), 400

    try:
        updated_transcription = update_transcription_name_use_case.execute(transcription_id=transcription_id,
                                                                           new_name=new_name)
        return jsonify({
            'id': updated_transcription.id,
            'audio_id': updated_transcription.audio_id,
            'name': updated_transcription.name,
            'text': updated_transcription.text,
            'language': updated_transcription.language,
            'segments': json.loads(updated_transcription.segments),
            'created_at': updated_transcription.created_at.isoformat() + 'Z' if updated_transcription.created_at else None,
            'isFavorite': updated_transcription.isFavorite,
            'summary': {
                'transcription_id': updated_transcription.summary.transcription_id,
                'id': updated_transcription.summary.id,
                'text': updated_transcription.summary.text
            } if updated_transcription.summary else None
        }), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@data_bp.route('/transcriptions/<int:transcription_id>', methods=['DELETE'])
@jwt_required()
def delete_transcription(transcription_id):
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    try:
        delete_transcription_use_case.execute(transcription_id=transcription_id)
        return '', 204
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@data_bp.route('/transcriptions/<int:transcription_id>/favorite', methods=['PUT'])
@jwt_required()
def favorite_transcription(transcription_id):
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    try:
        updated_transcription = favorite_transcription_use_case.execute(transcription_id=transcription_id)

        return jsonify({
            'id': updated_transcription.id,
            'audio_id': updated_transcription.audio_id,
            'name': updated_transcription.name,
            'text': updated_transcription.text,
            'language': updated_transcription.language,
            'segments': json.loads(updated_transcription.segments),
            'created_at': updated_transcription.created_at.isoformat() + 'Z' if updated_transcription.created_at else None,
            'isFavorite': updated_transcription.isFavorite,
            'summary': {
                'transcription_id': updated_transcription.summary.transcription_id,
                'id': updated_transcription.summary.id,
                'text': updated_transcription.summary.text
            } if updated_transcription.summary else None
        }), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@data_bp.route('/audio-files/<audio_id>', methods=['GET'])
@jwt_required()
def get_audio_file(audio_id):
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    try:
        # Use the GetAudioUseCase to retrieve the file
        audio_content, audio_format = get_audio_use_case.execute(user=user, audio_id=audio_id)

        # Create an in-memory stream from the binary content
        audio_stream = BytesIO(audio_content)

        # Determine the correct MIME type based on the format
        mime_types = {
            "mp3": "audio/mpeg",
            "wav": "audio/wav",
            "ogg": "audio/ogg",
            "flac": "audio/flac"
        }
        mimetype = mime_types.get(audio_format, "audio/mpeg")  # Default to "audio/mpeg" if the format is unknown

        # Stream the audio file as a response
        return send_file(
            audio_stream,
            mimetype=mimetype,
            as_attachment=False,
            download_name=f"{audio_id}.{audio_format}"  # Use the correct extension for the file name
        ), 200

    except FileNotFoundError:
        return jsonify({"message": "Audio file not found"}), 404
