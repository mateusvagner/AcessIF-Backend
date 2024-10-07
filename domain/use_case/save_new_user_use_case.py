import bcrypt

from database.database import db
from database.model.user import User


class SaveNewUserUseCase:
    def execute(self, name: str, email: str, password: str) -> User:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return new_user

