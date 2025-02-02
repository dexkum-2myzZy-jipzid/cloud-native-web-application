from flask import Blueprint, jsonify
from database.connection import get_db_connection

movies_bp = Blueprint('movies', __name__, url_prefix='/v1')

@movies_bp.route('/movie/<int:record_id>', methods=['GET'])
def get_movie(record_id):
    try:
        conn = get_db_connection()
        if conn is None or not conn.is_connected():
            response = jsonify({"error": "Service Unavailable"}), 503
            return response
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM movies WHERE movieId = %s", (record_id,))
        movie = cursor.fetchone()

        print(movie)
            
        if not movie:
            return jsonify({"error": "Movie Not Found"}), 400

        return jsonify({"movie": format_movie(movie)}), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

def format_movie(movie):
    return {
        "movieId": movie["movieId"],
        "title": movie["title"].strip(),
        "genres": movie["genres"],
    }