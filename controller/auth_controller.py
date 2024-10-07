import bcrypt

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from database.model.user import User
from domain.use_case.save_new_user_use_case import SaveNewUserUseCase

auth_bp = Blueprint('auth', __name__)

save_new_user_use_case = SaveNewUserUseCase()


@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        return jsonify({'message': 'User already exists'}), 400

    save_new_user_use_case.execute(name, email, password)
    access_token = create_access_token(identity=email)
    refresh_token = create_refresh_token(identity=email)

    return jsonify(access_token=access_token, refresh_token=refresh_token), 200


@auth_bp.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password):
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=email)
    refresh_token = create_refresh_token(identity=email)

    return jsonify(access_token=access_token, refresh_token=refresh_token), 200


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token), 200
