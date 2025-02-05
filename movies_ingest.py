import csv
from config import get_db_connection

CSV_FILE = 'ml-latest-small/movies.csv'

# Recreate movies table
def recreate_movies_table(cursor):
    cursor.execute("DROP TABLE IF EXISTS movies")
    cursor.execute("""
        CREATE TABLE movies (
            movieId INT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            genres VARCHAR(255)
        )
    """)

# Import CSV data into the database
def import_movies_to_db():
    try:
        # Connect to the database
        connection = get_db_connection()
        cursor = connection.cursor()

        # Recreate the table
        recreate_movies_table(cursor)

        # Read the CSV file and insert data
        with open(CSV_FILE, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cursor.execute("""
                    INSERT INTO movies (movieId, title, genres) 
                    VALUES (%s, %s, %s)
                """, (row['movieId'], row['title'], row['genres']))

        # Commit the transaction
        connection.commit()
        print("Movies data imported successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == "__main__":
    import_movies_to_db()
