import json


def lambda_handler(event, context):
    # get movie_id
    path_params = event.get("pathParameters") or {}
    movie_id_str = path_params.get("movie_id")

    # check movie_id
    if not movie_id_str:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "movie id is required"}),
        }

    # check movie_id type
    try:
        movie_id = int(movie_id_str)
    except ValueError:
        return {"statusCode": 400, "body": json.dumps({"error": "invalid movie id"})}

    # check movie_id range
    if movie_id < 1 or movie_id > 999999:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "movie id is out of range"}),
        }

    # successful response
    response_data = {
        "movie_id": movie_id,
        "poster_url": f"https://example.com/posters/{movie_id}.jpg",
        "poster_size": 1024000,
        "message": "post details fetched successfully",
    }

    # get content_type
    headers = event.get("headers", {})
    content_type = headers.get("Content-Type", "application/json")

    if "text/plain" in content_type:
        # text format
        body = f"movie_id: {movie_id}, poster_url: https://example.com/posters/{movie_id}.jpg, poster_size: 1024000, message: post details fetched successfully"
        return {
            "statusCode": 200,
            "body": body,
            "headers": {"Content-Type": "text/plain"},
        }
    else:
        # json format
        return {
            "statusCode": 200,
            "body": json.dumps(response_data),
            "headers": {"Content-Type": "application/json"},
        }
