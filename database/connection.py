import mysql.connector
from mysql.connector import Error
from .config import DatabaseConfig

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=DatabaseConfig.HOST,
            user=DatabaseConfig.USER,
            password=DatabaseConfig.PASSWORD,
            database=DatabaseConfig.NAME,
            connection_timeout=DatabaseConfig.CONNECTION_TIMEOUT,
        )
        if connection.is_connected():
            print("Successfully connected to the database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None