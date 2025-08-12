import secrets
import hmac
import hashlib
from logging import exception

import jwt
import json
from datetime import datetime, timedelta, timezone
from flask import current_app
from ..extension import redis_client
from typing import Optional, Union


def get_refresh_token_secret() -> bytes:
    return current_app.config["REFRESH_TOKEN_SECRET"].encode("utf-8")

def get_refresh_token_expiry_time() -> timedelta:
    return timedelta(days=current_app.config["REFRESH_TOKEN_TTL"])

def generate_jwt_token(user_id: str, username: str, email: str) -> str:
    payload = {
        "sub": user_id,
        "username": username,
        "email": email,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5)
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def decode_jwt_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def generate_custom_refresh_token(user_id: str) -> str:
    """
    Generates a secure custom refresh token with HMAC signing.
    """
    random_bytes = secrets.token_bytes(32)
    signature = hmac.new(
        get_refresh_token_secret(),
        random_bytes,
        hashlib.sha256
    ).hexdigest()
    token = f"{random_bytes.hex()}.{signature}"

    redis_client.setex(
        f"refresh_token:{token}",
        get_refresh_token_expiry_time(),
        user_id
    )
    return token


def validate_refresh_token(token: str) -> Optional[Union[int, str]]:
    """
    Verifies the token exists in Redis and has a valid HMAC signature.
    Returns user_id if valid, else None.
    """
    try:
        random_hex, signature = token.split(".")
        random_bytes = bytes.fromhex(random_hex)

        expected_signature = hmac.new(
            get_refresh_token_secret(),
            random_bytes,
            hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(expected_signature, signature):
            return None

        user_id = redis_client.get(f"refresh_token:{token}")
        return user_id
    except Exception as e:
        print(f"Unexpected error validating refresh token: {e}")
        return None
