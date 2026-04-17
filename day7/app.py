from flask import Flask, jsonify, request, redirect

from database import initialize_database
from url_service import URLService

app = Flask(__name__)
url_service = URLService()


def is_valid_url(url):
    return url.startswith("http://") or url.startswith("https://")


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Basic URL Shortener API is running",
        "endpoints": [
            "POST /shorten",
            "GET /urls",
            "GET /<short_code>"
        ],
        "next_improvements": [
            "click tracking",
            "custom short codes",
            "authentication",
            "delete short URLs"
        ]
    })


@app.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    if "original_url" not in data:
        return jsonify({"error": "Missing required field: original_url"}), 400

    original_url = str(data["original_url"]).strip()

    if not original_url:
        return jsonify({"error": "Original URL cannot be empty."}), 400

    if not is_valid_url(original_url):
        return jsonify({"error": "URL must start with http:// or https://"}), 400

    url_record = url_service.create_short_url(original_url)

    short_url = request.host_url.rstrip("/") + "/" + url_record["short_code"]

    return jsonify({
        "message": "Short URL created successfully.",
        "data": {
            "id": url_record["id"],
            "original_url": url_record["original_url"],
            "short_code": url_record["short_code"],
            "short_url": short_url,
            "created_at": url_record["created_at"]
        }
    }), 201


@app.route("/urls", methods=["GET"])
def get_urls():
    urls = url_service.get_all_urls()

    result = []
    for url in urls:
        result.append({
            "id": url["id"],
            "original_url": url["original_url"],
            "short_code": url["short_code"],
            "short_url": request.host_url.rstrip("/") + "/" + url["short_code"],
            "created_at": url["created_at"]
        })

    return jsonify(result), 200


@app.route("/<short_code>", methods=["GET"])
def redirect_to_original_url(short_code):
    url_record = url_service.get_url_by_short_code(short_code)

    if not url_record:
        return jsonify({"error": "Short URL not found."}), 404

    return redirect(url_record["original_url"])
    

if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)
