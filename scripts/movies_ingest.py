import sys
import os

# Get the absolute path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the project root directory (assuming scripts/ is a subdirectory of the project root)
project_root = os.path.dirname(script_dir)
# Add the project root to the Python path
sys.path.insert(0, project_root)

import csv
from database.connection import get_db_connection

CSV_FILE = 'ml-latest-small/movies.csv'

def recreate_movies_table(cursor):
    cursor.execute("DROP TABLE IF EXISTS movies")
    cursor.execute("""
        CREATE TABLE movies (
            movieId INT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            genres VARCHAR(255)
        )
    """)

def import_movies_to_db():
    try:
         # Connect to the database
        connection = get_db_connection()
        cursor = connection.cursor()
        # Recreate the table
        recreate_movies_table(cursor)
            
        # Read CSV and insert data
        with open(CSV_FILE, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cursor.execute("""
                    INSERT INTO movies (movieId, title, genres) 
                    VALUES (%s, %s, %s)
                """, (row['movieId'], row['title'], row['genres']))

        # Commit the transaction
        connection.commit()           
        print("✅ Movies data imported successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    import_movies_to_db()