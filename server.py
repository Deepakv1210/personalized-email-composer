
from flask import Flask, request, jsonify
from flask_cors import CORS
from response_generator import generate_email_response

app = Flask(__name__)
CORS(app)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    subject = data.get("subject", "")
    body = data.get("body", "")
    compose_type = data.get("composeType", "new")
    if compose_type == "reply":
        query = f"(Replying) Subject: {subject}\nThread Excerpt: {body}"
    else:
        # It's a new email
        query = f"(New) Subject: {subject}\nUser typed: {body}"

    ai_response = generate_email_response(query, compose_type=compose_type)

    return jsonify({"suggestion": ai_response})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
