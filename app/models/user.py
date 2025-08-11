from .. import database

import uuid

from ..utils.encrypt import hash_password , check_password


class User(database.Model):
    __tablename__ = "users"
    user_id = database.Column(database.String(100), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = database.Column(database.String(100), unique = True, nullable=False)
    email = database.Column(database.String(100), unique = True, nullable=False )
    password_hash = database.Column(database.String(255),nullable=False )

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self , password):
        self.password_hash = hash_password(password)

    def check_password(self , password):
        return check_password(password,self.password_hash)