from flask import Blueprint, json
from database.connection import db_cursor

movies_bp = Blueprint('movies', __name__, url_prefix='/v1')

@movies_bp.route('/movie/<int:record_id>', methods=['GET'])
def get_movie(record_id):
    try:
        with db_cursor() as cursor:
            cursor.execute(
                "SELECT movieId, title, genres FROM movies WHERE movieId = %s",
                (record_id,)
            )
            movie = cursor.fetchone()

            if not movie:
                return {"error": "Movie Not Found"}, 404

            return {"movie": format_movie(movie)}, 200
    except Exception as e:
        return {"error": "Internal Server Error", "details": str(e)}, 500

def format_movie(movie):
    return {
        "movieId": movie["movieId"],
        "title": movie["title"].strip(),
        "genres": movie["genres"].split('|')
    }