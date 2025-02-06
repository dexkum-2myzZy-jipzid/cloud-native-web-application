import csv
from collections import defaultdict


def process_large_movies(input_file):
    # Phase 1: Collect all unique genres
    genre_set = set()

    # First pass: collect all genres (streaming)
    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            genres = row["genres"].split("|")
            for genre in genres:
                genre_set.add(genre)

    # Generate genre mapping table (sorted alphabetically)
    sorted_genres = sorted(genre_set)
    genre_to_id = {genre: idx + 1 for idx, genre in enumerate(sorted_genres)}

    # Phase 2: Stream process data
    with open(input_file, "r", encoding="utf-8") as f_in, open(
        "movies.csv", "w", newline="", encoding="utf-8"
    ) as f_movies, open(
        "genres.csv", "w", newline="", encoding="utf-8"
    ) as f_genres, open(
        "movies_genres.csv", "w", newline="", encoding="utf-8"
    ) as f_relation:

        reader = csv.DictReader(f_in)

        # Initialize writers
        movies_writer = csv.writer(f_movies)
        movies_writer.writerow(["movieId", "title"])

        genres_writer = csv.writer(f_genres)
        genres_writer.writerow(["genreId", "genre"])

        relation_writer = csv.writer(f_relation)
        relation_writer.writerow(["movieId", "genreId"])

        # Write genre data
        for genre in sorted_genres:
            genres_writer.writerow([genre_to_id[genre], genre])

        # Process movie data row by row
        for row in reader:
            # Write to movies table
            movies_writer.writerow([row["movieId"], row["title"]])

            # Process genres relations
            genres = row["genres"].split("|")
            for genre in genres:
                if genre in genre_to_id:
                    relation_writer.writerow([row["movieId"], genre_to_id[genre]])


if __name__ == "__main__":
    process_large_movies("ml-32m/movies.csv")
