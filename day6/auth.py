from functools import wraps
from flask import request, jsonify
from user_service import UserService

user_service = UserService()


def extract_bearer_token(auth_header):
    if not auth_header:
        return None

    parts = auth_header.split()

    if len(parts) != 2 or parts[0] != "Bearer":
        return None

    return parts[1]


def require_auth(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        token = extract_bearer_token(auth_header)

        if not token:
            return jsonify({"error": "Authorization token is missing or invalid."}), 401

        user = user_service.get_user_by_token(token)
        if not user:
            return jsonify({"error": "Unauthorized. Invalid token."}), 401

        request.current_user = user
        return route_function(*args, **kwargs)

    return wrapper