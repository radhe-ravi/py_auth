from functools import wraps
from flask import request, jsonify
from ..services.token_service import decode_jwt_token

def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"msg": "Missing or invalid token"}), 401

        token = auth_header.split(" ")[1]
        payload = decode_jwt_token(token)
        if not payload:
            return jsonify({"msg": "Invalid or expired token"}), 401

        request.user = payload
        return f(*args, **kwargs)
    return decorated_function
