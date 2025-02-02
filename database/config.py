import os
from dotenv import load_dotenv

# Load .env file from the project root
load_dotenv()

class DatabaseConfig:
    """Database configuration class"""
    HOST = os.getenv('DB_HOST')
    USER = os.getenv('DB_USER')
    PASSWORD = os.getenv('DB_PASSWORD')
    NAME = os.getenv('DB_NAME')
    POOL_NAME = "movie_pool"
    POOL_SIZE = 5
    CONNECTION_TIMEOUT = 3