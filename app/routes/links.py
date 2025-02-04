from flask import Blueprint, jsonify, request
from database.connection import get_db_connection

links_bp = Blueprint('links', __name__, url_prefix='/v1')

@links_bp.route('/link/<int:movie_id>', methods=['GET'])
@links_bp.route('/link', methods=['GET'])
def get_link(movie_id=None):
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
            # Query link information
            cursor.execute("""
                SELECT movieId, imdbId, tmdbId 
                FROM links 
                WHERE movieId = %s
            """, (movie_id,))
            link = cursor.fetchone()

            if not link:
                return jsonify({"error": "Link not found"}), 404

        # Build response
        return jsonify({
            "movieId": link['movieId'],
            "imdbId": link['imdbId'],
            "tmdbId": link['tmdbId']
        })

    except ValueError:
        return jsonify({"error": "Invalid movie identifier format"}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()