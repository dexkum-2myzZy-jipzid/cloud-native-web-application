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
    CONNECTION_TIMEOUT = 3