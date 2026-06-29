from flask import Flask, request, jsonify, redirect
import random
import string
import db
from prometheus_flask_exporter import PrometheusMetrics
app = Flask(__name__)
metrics = PrometheusMetrics(app)


def generate_code(length=6):
    return ''.join(random.choices
                   (string.ascii_letters + string.digits, k=length))


@app.route('/health')
def health():
    return 'OK'


@app.route("/shorten", methods=["POST"])
def shorten():
    data = request.get_json()
    original_url = data.get("url")

    code = generate_code()

    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO links (short_code, original_url) VALUES (%s, %s)
        """,
        (code, original_url)
    )
    conn.commit()
    conn.close()

    return jsonify({"short_code": code}), 201


@app.route("/<code>")
def go_to_url(code):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT original_url FROM links WHERE short_code = %s
        """,
        (code,)
    )
    result = cursor.fetchone()
    conn.close()

    if not result:
        return jsonify({"error": "URL not found"}), 404

    original_url = result[0]
    return redirect(original_url)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)