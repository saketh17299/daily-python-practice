from flask import Flask, jsonify, request

from api_key_service import ApiKeyService
from rate_limiter import RateLimiter

app = Flask(__name__)

api_service = ApiKeyService()
rate_limiter = RateLimiter(limit=5, window_seconds=60)


def get_api_key_from_request():
    return request.headers.get("x-api-key")


def require_api_key(func):
    def wrapper(*args, **kwargs):
        api_key = get_api_key_from_request()

        if not api_key:
            return jsonify({"error": "API key missing"}), 401

        if not api_service.is_valid_key(api_key):
            return jsonify({"error": "Invalid API key"}), 403

        if not rate_limiter.is_allowed(api_key):
            return jsonify({"error": "Rate limit exceeded"}), 429

        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "API Gateway Simulation",
        "endpoints": [
            "POST /generate-key",
            "GET /protected"
        ],
        "rate_limit": "5 requests per minute"
    })


@app.route("/generate-key", methods=["POST"])
def generate_key():
    key = api_service.generate_api_key()
    return jsonify({"api_key": key}), 201


@app.route("/protected", methods=["GET"])
@require_api_key
def protected():
    return jsonify({
        "message": "You accessed a protected endpoint!"
    }), 200


if __name__ == "__main__":
    app.run(debug=True)