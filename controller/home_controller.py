from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request

from database.model.user import User

home_bp = Blueprint('transcript', __name__)


@home_bp.route('/home', methods=['GET'])
@jwt_required()
def home():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    return jsonify(logged_in_as=user.name), 200


@home_bp.route('/optional', methods=['GET'])
def optional():
    verify_jwt_in_request(optional=True)
    current_user_email = get_jwt_identity()

    if current_user_email:
        user = User.query.filter_by(email=current_user_email).first()
        return jsonify(message=f'Hello {user.name}, you are authenticated'), 200
    else:
        return jsonify(message='Hello Guest, you are not authenticated'), 200
