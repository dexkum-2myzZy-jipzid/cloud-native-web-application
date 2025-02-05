from flask import Flask, jsonify
from mysql.connector import Error
from config import get_db_connection

app = Flask(__name__)


# Healthcheck endpoint
@app.route("/v1/healthcheck", methods=["GET"])
def healthcheck():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"status": "Database Unavailable"}), 503

        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchall()
        return jsonify({"status": "OK"}), 200
    except Error as e:
        return jsonify({"status": "Database Unavailable", "error": str(e)}), 503
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


# Movie query endpoint
@app.route("/v1/movie/<int:record_id>", methods=["GET"])
def get_movie(record_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM movies WHERE movieId = %s", (record_id,))
        movie = cursor.fetchone()

        if not movie:
            return jsonify({"error": "Movie Not Found"}), 400

        return jsonify({"movie": movie}), 200
    except Error as e:
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
