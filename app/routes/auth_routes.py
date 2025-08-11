from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from .. import database
from ..models.user import User
from flask_jwt_extended import create_access_token
auth_bp = Blueprint('auth', __name__)


def get_data():
    data = request.get_json() or {}
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not password:
        raise ValueError("Password is required.")
    if not (username or email):
        raise ValueError("Either username or email is required.")
    return username, email, password


def is_username_email_taken(username, email):
    return User.query.filter(
        or_(User.username == username, User.email == email)
    ).first() is not None

def get_user_by_username_or_email(username, email):
    return User.query.filter(
        or_(User.username == username, User.email == email)
    ).first()



def create_user(username, email, password):
    user = User(username=username, email=email)
    user.set_password(password)
    database.session.add(user)
    database.session.commit()
    return user


@auth_bp.route('/register', methods=['POST'])
def register():

    try:
        username, email, password = get_data()
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400
    if is_username_email_taken(username, email):
        return jsonify({"msg": "Username or Email already exists"}), 409

    create_user(username, email, password)
    return jsonify({"msg": "User registered successfully"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    username,email, password = get_data()
    user = get_user_by_username_or_email(username, email)
    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.user_id))
        return  jsonify(access_token=access_token)
    return jsonify({"msg": "Bad username or password"}), 401
