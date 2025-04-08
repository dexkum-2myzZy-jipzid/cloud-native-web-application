import json
import os
import requests

# get TMDB TOKEN from env
TMDB_READ_TOKEN = os.environ.get("TMDB_READ_TOKEN", "")


def lambda_handler(event, context):
    # get movie id
    path_params = event.get("pathParameters") or {}
    movie_id_str = path_params.get("movie_id")

    # check movie_id
    if not movie_id_str:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "movie id is required"}),
        }

    try:
        movie_id = int(movie_id_str)
    except ValueError:
        return {"statusCode": 400, "body": json.dumps({"error": "invalid movie id"})}

    if movie_id < 1 or movie_id > 999999:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "movie id is out of range"}),
        }

    # default response
    default_response = {
        "movie_id": movie_id,
        "poster_url": f"https://example.com/posters/{movie_id}.jpg",
        "poster_size": 1024000,
        "message": "post details fetched successfully",
    }

    # call TMDB API
    try:
        tmdb_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        headers = {"Authorization": f"Bearer {TMDB_READ_TOKEN}"}
        tmdb_response = requests.get(tmdb_url, headers=headers, timeout=3)
        if tmdb_response.status_code == 200:
            tmdb_data = tmdb_response.json()
            poster_path = tmdb_data.get("poster_path")
            if poster_path:
                # real poster URL
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                default_response["poster_url"] = poster_url
                default_response["message"] = "real poster details fetched successfully"
            else:
                default_response["message"] = (
                    "poster path not available from TMDB, using default poster"
                )
        else:
            default_response["message"] = (
                f"TMDB API call failed with status {tmdb_response.status_code}, using default poster"
            )
    except Exception as e:
        default_response["message"] = (
            f"Exception occurred: {str(e)}, using default poster"
        )

    # check content type
    headers_req = event.get("headers", {})
    content_type = headers_req.get("Content-Type", "application/json")

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
