from flask import Blueprint, jsonify, request
from database.connection import get_db_connection

ratings_bp = Blueprint('ratings', __name__, url_prefix='/v1')

@ratings_bp.route('/rating/<int:movie_id>', methods=['GET'])
@ratings_bp.route('/rating', methods=['GET'])
def get_movie_rating(movie_id=None):
    conn = None
    try:
        # Handle parameters
        if movie_id is None:
            movie_id = request.args.get('id', type=int)
        
        if not movie_id:
            return jsonify({"error": "Missing movie identifier"}), 400

        # Database connection
        conn = get_db_connection()
        if conn is None or not conn.is_connected():
            return jsonify({"error": "Service Unavailable"}), 503

        with conn.cursor(dictionary=True) as cursor:
            # Query average rating
            cursor.execute("""
                SELECT 
                    movieId,
                    ROUND(AVG(rating), 5) AS average_rating 
                FROM ratings 
                WHERE movieId = %s
                GROUP BY movieId
            """, (movie_id,))
            result = cursor.fetchone()

            if not result:
                return jsonify({"error": "No ratings found for this movie"}), 404

        # Build response
        return jsonify({
            "movieId": result['movieId'],
            "average_rating": float(result['average_rating'])
        })

    except ValueError:
        return jsonify({"error": "Invalid movie identifier format"}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()