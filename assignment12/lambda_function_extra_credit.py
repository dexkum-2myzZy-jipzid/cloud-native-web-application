import json
import os
import requests

# get TMDB Read Token
TMDB_READ_TOKEN = os.environ.get("TMDB_READ_TOKEN", "")


def validate_movie_id(event):
    path_params = event.get("pathParameters") or {}
    movie_id_str = path_params.get("movie_id")
    if not movie_id_str:
        return None, {
            "statusCode": 400,
            "body": json.dumps({"error": "movie id is required"}),
        }
    try:
        movie_id = int(movie_id_str)
    except ValueError:
        return None, {
            "statusCode": 400,
            "body": json.dumps({"error": "invalid movie id"}),
        }
    if movie_id < 1 or movie_id > 999999:
        return None, {
            "statusCode": 400,
            "body": json.dumps({"error": "movie id is out of range"}),
        }
    return movie_id, None


def get_auth_token():
    user_email = os.environ.get("MOVIE_USER_EMAIL", "")
    user_password = os.environ.get("MOVIE_USER_PASSWORD", "")
    if not user_email or not user_password:
        raise Exception("User credentials (email/password) not configured")

    auth_url = "http://api.dexmario.me/v1/login"
    auth_payload = {"email": user_email, "password": user_password}
    auth_response = requests.post(auth_url, json=auth_payload, timeout=3)
    if auth_response.status_code != 200:
        raise Exception("Failed to authenticate with movie API")
    auth_data = auth_response.json()
    token = auth_data.get("token")
    if not token:
        raise Exception("Authentication token not found in response")
    return token


def fetch_imdb_id(movie_id, token):
    movie_url = f"http://api.dexmario.me/v1/link/{movie_id}"
    headers_movie = {"Authorization": f"Bearer {token}"}
    movie_response = requests.get(movie_url, headers=headers_movie, timeout=3)
    if movie_response.status_code != 200:
        raise Exception("Failed to fetch tmdbId from movie API")
    movie_data = movie_response.json()
    tmdb_Id = movie_data.get("tmdbId")
    if not tmdb_Id:
        raise Exception("tmdbId not found in movie API response")
    return tmdb_Id


def fetch_tmdb_poster(tmdb_Id):
    tmdb_url = f"https://api.themoviedb.org/3/movie/{tmdb_Id}"
    headers_tmdb = {"Authorization": f"Bearer {TMDB_READ_TOKEN}"}
    tmdb_response = requests.get(tmdb_url, headers=headers_tmdb, timeout=3)
    if tmdb_response.status_code != 200:
        raise Exception(f"TMDB API call failed with status {tmdb_response.status_code}")
    tmdb_data = tmdb_response.json()
    poster_path = tmdb_data.get("poster_path")
    if poster_path:
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        return poster_url, "post details fetched successfully"
    else:
        return None, "poster path not available from TMDB, using default poster"


def build_response(default_response, content_type):
    if "text/plain" in content_type:
        body = (
            f"movie_id: {default_response['movie_id']}, poster_url: {default_response['poster_url']}, "
            f"poster_size: {default_response['poster_size']}, message: {default_response['message']}"
        )
        return {
            "statusCode": 200,
            "body": body,
            "headers": {"Content-Type": "text/plain"},
        }
    else:
        return {
            "statusCode": 200,
            "body": json.dumps(default_response),
            "headers": {"Content-Type": "application/json"},
        }


def lambda_handler(event, context):
    # 1. validate movie_id
    movie_id, error_response = validate_movie_id(event)
    if error_response:
        return error_response

    default_response = {
        "movie_id": movie_id,
        "poster_url": f"https://example.com/posters/{movie_id}.jpg",
        "poster_size": 1024000,
        "message": "post details fetched successfully",
    }

    try:
        # 2. get token
        token = get_auth_token()
        # 3. Fetch tmdbId using the token
        tmdb_Id = fetch_imdb_id(movie_id, token)
        # 4. Fetch poster details from TMDB API using tmdbId
        poster_url, tmdb_message = fetch_tmdb_poster(tmdb_Id)
        if poster_url:
            default_response["poster_url"] = poster_url
        default_response["message"] = tmdb_message
    except Exception as e:
        default_response["message"] = (
            f"Exception occurred: {str(e)}, using default poster"
        )

    # check content type
    headers_req = event.get("headers", {})
    content_type = headers_req.get("Content-Type", "application/json")
    return build_response(default_response, content_type)
