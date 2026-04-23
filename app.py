from flask import Flask, jsonify, render_template, request

from checker.strength import evaluate_password

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/check")
def check_password():
    payload = request.get_json(silent=True) or {}
    password = payload.get("password", "")
    result = evaluate_password(password)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
