from flask import Flask, jsonify, make_response, request
from mysql.connector import Error
from config import get_db_connection
from collections import OrderedDict
import json


app = Flask(__name__)


def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@app.route("/v1/healthcheck", methods=["GET"])
def healthcheck():
    if request.args or request.form:
        response = make_response(jsonify({"error": "Bad Request"}), 400)
        return set_response_headers(response)

    db_connection = get_db_connection()
    if db_connection and db_connection.is_connected():
        db_connection.close()
        response = make_response(jsonify({"status": "OK"}), 200)
    else:
        response = make_response(jsonify({"error": "Service Unavailable"}), 503)
    
    return set_response_headers(response)

# Handle unsupported endpoints and methods
@app.errorhandler(404)
@app.errorhandler(405)
def handle_unsupported(e):
    response = make_response('', 400)
    return set_response_headers(response)

@app.route("/v1/movie/<int:record_id>", methods=["GET"])
def get_movie(record_id):
    try:
        conn = get_db_connection()
        if conn is None or not conn.is_connected():
            response = make_response(jsonify({"error": "Service Unavailable"}), 503)
            return set_response_headers(response)
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM movies WHERE movieId = %s", (record_id,))
        movie = cursor.fetchone()

        if not movie:
            response = make_response(jsonify({"error": "Movie Not Found"}), 400)
            return set_response_headers(response)

        formatted_movie = {
            "movieId": movie["movieId"],
            "title": movie["title"],
            "genres": movie["genres"]
        }
        response_data = json.dumps({"movie": formatted_movie}, separators=(',', ':'))
        response = make_response(response_data, 200)
        response.headers['Content-Type'] = 'application/json'
        return set_response_headers(response)
    except Error as e:
        response = make_response(jsonify({"error": "Internal Server Error", "details": str(e)}), 500)
        return set_response_headers(response)
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
