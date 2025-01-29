from flask import Flask, jsonify, make_response, request
from mysql.connector import Error
from config import get_db_connection

app = Flask(__name__)


# Healthcheck endpoint
@app.after_request
def add_no_cache_header(response):
    response.headers["Cache-Control"] = "no-cache"
    return response

@app.route("/v1/healthcheck", methods=["GET"])
def healthcheck():
    if request.args or request.form:
        return make_response(jsonify({"error": "Bad Request"}), 400)

    db_connection = get_db_connection()
    if db_connection and db_connection.is_connected():
        db_connection.close()
        return make_response(jsonify({"status": "OK"}), 200)
    else:
        return make_response(jsonify({"error": "Service Unavailable"}), 503)


# Movie query endpoint
@app.route("/v1/movie/<int:record_id>", methods=["GET"])
def get_movie(record_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM movies WHERE movieId = %s", (record_id,))
        movie = cursor.fetchone()

        if not movie:
            response = make_response(jsonify({"error": "Movie Not Found"}), 400)
            return response

        formatted_movie = {
            "movieId": movie["movieId"],
            "title": movie["title"],
            "genres": movie["genres"]
        }

        response = make_response(jsonify({"movie": formatted_movie}), 200)
        return response
    except Error as e:
        response = make_response(jsonify({"error": "Internal Server Error", "details": str(e)}), 500)
        return response
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
