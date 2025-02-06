import csv
from collections import defaultdict
import random
import time
from tqdm import tqdm


class NormalizationValidator:
    def __init__(self, original_file, movies_file, genres_file, relation_file):
        self.original_file = original_file
        self.movies_file = movies_file
        self.genres_file = genres_file
        self.relation_file = relation_file

        # Data storage
        self.original_data = defaultdict(dict)
        self.normalized_data = {
            "movies": set(),
            "genres": set(),
            "relations": defaultdict(set),
        }

        # Metrics
        self.metrics = {
            "total_movies": 0,
            "total_genres": 0,
            "duplicate_movies": 0,
            "orphan_relations": 0,
            "mismatch_records": 0,
            "sample_checks": 0,
            "sample_errors": 0,
        }

    def _load_original_data(self):
        """Load original data"""
        with open(self.original_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in tqdm(reader, desc="Loading original data"):
                movie_id = row["movieId"]
                genres = set(row["genres"].split("|")) - {""}
                self.original_data[movie_id] = genres
                self.metrics["total_movies"] += 1

    def _load_normalized_data(self):
        """Load normalized data"""
        # Load movies
        with open(self.movies_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in tqdm(reader, desc="Validating Movies data"):
                movie_id = row["movieId"]
                if movie_id in self.normalized_data["movies"]:
                    self.metrics["duplicate_movies"] += 1
                self.normalized_data["movies"].add(movie_id)

        # Load genres
        with open(self.genres_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in tqdm(reader, desc="Validating Genres data"):
                genre_id = row["genreId"]
                genre_name = row["name"]
                self.normalized_data["genres"].add((genre_id, genre_name))

        # Load relations and build reverse index
        genre_map = {name: gid for gid, name in self.normalized_data["genres"]}
        with open(self.relation_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in tqdm(reader, desc="Validating relations"):
                movie_id = row["movieId"]
                genre_id = row["genreId"]
                self.normalized_data["relations"][movie_id].add(genre_id)

                # Validate genre existence
                if genre_id not in genre_map.values():
                    self.metrics["orphan_relations"] += 1

    def _validate_completeness(self):
        """Validate completeness"""
        # Check movie count consistency
        original_count = self.metrics["total_movies"]
        normalized_count = len(self.normalized_data["movies"])

        print(f"\nCompleteness check:")
        print(f"Original movie count: {original_count}")
        print(f"New Movies table count: {normalized_count}")

        if original_count != normalized_count:
            print(f"⚠️ Data inconsistency! Difference: {abs(original_count - normalized_count)}")

        # Check all original movie IDs exist
        missing_movies = set(self.original_data.keys()) - self.normalized_data["movies"]
        if missing_movies:
            print(f"⚠️ Missing movie records: {len(missing_movies)}")
            print("Example missing IDs:", list(missing_movies)[:5])

    def _validate_consistency(self):
        """Validate consistency"""
        print("\nConsistency check:")
        # Check movie IDs in relations table
        relation_movies = set(self.normalized_data["relations"].keys())
        missing_in_relations = self.normalized_data["movies"] - relation_movies
        if missing_in_relations:
            print(f"⚠️ {len(missing_in_relations)} movies missing genre relations")

        # Check genre existence in relations table
        all_genre_ids = {gid for gid, _ in self.normalized_data["genres"]}
        found_bad_genres = 0
        for movie_id, genres in self.normalized_data["relations"].items():
            invalid = genres - all_genre_ids
            if invalid:
                found_bad_genres += len(invalid)
        if found_bad_genres:
            print(f"⚠️ Found {found_bad_genres} invalid genre relations")

    def _random_sample_check(self, sample_size=100):
        """Random sample check"""
        print(f"\nRandom sample check ({sample_size} samples):")
        genre_id_to_name = {gid: name for gid, name in self.normalized_data["genres"]}
        sample_ids = random.sample(
            list(self.original_data.keys()), min(sample_size, len(self.original_data))
        )

        error_count = 0
        for movie_id in tqdm(sample_ids):
            original_genres = self.original_data[movie_id]
            normalized_genres = self.normalized_data["relations"].get(movie_id, set())

            # Convert IDs to genre names
            normalized_names = {
                genre_id_to_name[gid]
                for gid in normalized_genres
                if gid in genre_id_to_name
            }

            if original_genres != normalized_names:
                error_count += 1
                if error_count <= 3:  # Show first 3 errors
                    print(f"\nError example (MovieID: {movie_id}):")
                    print("Original genres:", original_genres)
                    print("Current genres:", normalized_names)

        self.metrics["sample_checks"] = len(sample_ids)
        self.metrics["sample_errors"] = error_count
        accuracy = (1 - error_count / len(sample_ids)) * 100
        print(f"Sample accuracy: {accuracy:.2f}%")

    def run_validation(self):
        """Run full validation process"""
        start_time = time.time()

        self._load_original_data()
        self._load_normalized_data()

        self._validate_completeness()
        self._validate_consistency()
        self._random_sample_check()

        # Print summary report
        print("\nValidation summary:")
        print(f"Total movies processed: {self.metrics['total_movies']}")
        print(f"Duplicate movie records: {self.metrics['duplicate_movies']}")
        print(f"Invalid genre relations: {self.metrics['orphan_relations']}")
        print(
            f"Sample check error rate: {self.metrics['sample_errors']}/{self.metrics['sample_checks']}"
        )
        print(f"Total time: {time.time()-start_time:.2f} seconds")


if __name__ == "__main__":
    validator = NormalizationValidator(
        original_file="original_movies.csv",
        movies_file="movies.csv",
        genres_file="genres.csv",
        relation_file="movies_genres.csv",
    )
    validator.run_validation()
