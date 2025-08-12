from flask import Blueprint, request, jsonify, Response
from sqlalchemy import or_
from .. import database
from ..models.user import User
from ..services.token_service import generate_jwt_token, generate_custom_refresh_token
from app.extension import redis_client

auth_bp = Blueprint('auth', __name__)

def get_data() -> tuple[str | None, str | None, str]:
    """
    Extracts username, email, and password from JSON request.
    Returns:
        tuple: (username, email, password)
    """
    data = request.get_json() or {}
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not password:
        raise ValueError("Password is required.")
    if not (username or email):
        raise ValueError("Either username or email is required.")
    return username, email, password


def is_username_email_taken(username: str | None, email: str | None) -> bool:
    """
    Checks if the username or email is already taken.
    """
    return User.query.filter(
        or_(User.username == username, User.email == email)
    ).first() is not None


def get_user_by_username_or_email(username: str | None, email: str | None) -> User | None:
    """
    Retrieves a user by username or email.
    """
    return User.query.filter(
        or_(User.username == username, User.email == email)
    ).first()


def create_user(username: str, email: str, password: str) -> User:
    """
    Creates a new user in the database.
    """
    user = User(username=username, email=email)
    user.set_password(password)
    database.session.add(user)
    database.session.commit()
    return user


@auth_bp.route('/register', methods=['POST'])
def register() -> tuple[Response, int]:
    """
    User registration endpoint.
    """
    try:
        username, email, password = get_data()
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400
    if is_username_email_taken(username, email):
        return jsonify({"msg": "Username or Email already exists"}), 409

    create_user(username, email, password)
    return jsonify({"msg": "User registered successfully"}), 201


@auth_bp.route('/login', methods=['POST'])
def login() -> tuple[Response, int]:
    """
    User login endpoint.
    """
    username, email, password = get_data()
    user = get_user_by_username_or_email(username, email)
    if user and user.validate_password(password):
        access_token = generate_jwt_token(user.user_id, user.username, user.email)
        refresh_token = generate_custom_refresh_token(user.user_id)
        return jsonify(
            access_token=access_token,
            refresh_token = refresh_token
        ), 200
    return jsonify({"msg": "Bad username or password"}), 401


@auth_bp.route("/refresh", methods=["POST"])
def refresh() -> tuple[Response, int]:
    data = request.get_json()
    refresh_token = data.get("refresh_token")

    if not refresh_token:
        return jsonify({"msg": "Missing refresh token"}) , 400

    # CHECK IN REDIS
    user_id = redis_client.get(f"refresh_token:{refresh_token}")

    if not user_id:
        return jsonify({"msg": "Invalid or expired refresh token"}) , 401

    user = User.query.get(user_id)
    new_access_token = generate_jwt_token(user.user_id, user.username, user.email)

    return jsonify({
        "access_token": new_access_token
    }), 200



