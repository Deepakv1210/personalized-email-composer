from flask import Flask, request, jsonify
from flask_cors import CORS
from response_generator import generate_email_response

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    subject = data.get("subject", "")
    body = data.get("body", "")

    query = f"Subject: {subject}\nBody: {body}"
    ai_response = generate_email_response(query)

    return jsonify({"suggestion": ai_response})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
