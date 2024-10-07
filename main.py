import os
from dotenv import load_dotenv
from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager

from controller.auth_controller import auth_bp
from controller.data_controller import data_bp
from controller.home_controller import home_bp
from controller.summarize_controller import summarize_bp
from controller.transcribe_controller import transcribe_bp
from database.database import db


def create_app():
    load_dotenv()

    flask_app = Flask(__name__)

    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    flask_app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    flask_app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
    flask_app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=15)

    flask_app.register_blueprint(home_bp)
    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(transcribe_bp)
    flask_app.register_blueprint(data_bp)
    flask_app.register_blueprint(summarize_bp)

    init_db(flask_app)
    init_jwt(flask_app)

    return flask_app


def init_db(flask_app):
    db.init_app(flask_app)
    with flask_app.app_context():
        # db.drop_all()  # TODO remove this when running for real
        db.create_all()


def init_jwt(flask_app):
    jwt = JWTManager(flask_app)
    return jwt


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')  # TODO - Change debug mode and host when running on prod
