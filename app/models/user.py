from .. import database

import uuid

from ..utils.security import generate_hash_password,verify_password_with_hashed_password


class User(database.Model):
    __tablename__ = "users"
    user_id = database.Column(database.String(100), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = database.Column(database.String(100), unique = True, nullable=False)
    email = database.Column(database.String(100), unique = True, nullable=False )
    password_hash = database.Column(database.String(255),nullable=False )

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self , password):
        self.password_hash = generate_hash_password(password)

    def validate_password(self , password):
        return verify_password_with_hashed_password(password,self.password_hash)