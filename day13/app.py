from functools import wraps
from flask import Flask, jsonify, request

from api_key_service import ApiKeyService
from database import initialize_database
from rate_limiter import RateLimiter

app = Flask(__name__)

api_service = ApiKeyService()
rate_limiter = RateLimiter(limit=5, window_seconds=60)


def get_api_key_from_request():
    return request.headers.get("x-api-key")


def require_api_key(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        api_key = get_api_key_from_request()

        if not api_key:
            return jsonify({"error": "API key missing"}), 401

        if not api_service.is_valid_key(api_key):
            return jsonify({"error": "Invalid or inactive API key"}), 403

        if not rate_limiter.is_allowed(api_key):
            return jsonify({"error": "Rate limit exceeded"}), 429

        return route_function(*args, **kwargs)

    return wrapper


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "API Gateway Simulation with Persistent API Keys",
        "endpoints": [
            "POST /generate-key",
            "GET /keys",
            "GET /protected"
        ],
        "rate_limit": "5 requests per minute per key"
    })


@app.route("/generate-key", methods=["POST"])
def generate_key():
    data = request.get_json(silent=True) or {}
    label = data.get("label")

    key = api_service.generate_api_key(label=label)

    return jsonify({
        "message": "API key generated successfully.",
        "data": key
    }), 201


@app.route("/keys", methods=["GET"])
def get_keys():
    keys = api_service.get_all_keys()
    return jsonify(keys), 200


@app.route("/protected", methods=["GET"])
@require_api_key
def protected():
    return jsonify({
        "message": "You accessed a protected endpoint!"
    }), 200


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)