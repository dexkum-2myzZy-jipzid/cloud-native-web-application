import mysql.connector.pooling
from mysql.connector import Error
from contextlib import contextmanager
from .config import DatabaseConfig

class ConnectionPool:
    """MySQL connection pool singleton"""
    _instance = None

    @classmethod
    def get_pool(cls):
        """Create or get the MySQL connection pool singleton"""
        if not cls._instance:
            try:
                cls._instance = mysql.connector.pooling.MySQLConnectionPool(
                    pool_name=DatabaseConfig.POOL_NAME,
                    pool_size=DatabaseConfig.POOL_SIZE,
                    host=DatabaseConfig.HOST,
                    user=DatabaseConfig.USER,
                    password=DatabaseConfig.PASSWORD,
                    database=DatabaseConfig.NAME,
                    connection_timeout=DatabaseConfig.CONNECTION_TIMEOUT
                )
                print("✅ Database connection pool initialized")
            except Error as e:
                print(f"❌ Failed to create connection pool: {e}")
                raise
        return cls._instance

def get_db_connection():
    """Get a database connection from the pool"""
    try:
        return ConnectionPool.get_pool().get_connection()
    except Error as e:
        print(f"❌ Failed to get database connection: {e}")
        raise

def close_all_connections():
    """Close all database connections (for maintenance or testing)"""
    if ConnectionPool._instance:
        ConnectionPool._instance.close()
        print("🛑 All database connections closed")

def init_database(app):
    """Initialize the database connection pool and perform a health check"""
    try:
        # Trigger connection pool initialization
        ConnectionPool.get_pool()
        # Manually verify database connection
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        if result[0] != 1:
            raise RuntimeError("Database health check failed")
        print("✅ Database connection validated")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Database initialization failed: {str(e)}")
        raise

@contextmanager
def db_cursor(commit: bool = False):
    """Database cursor context manager (automatic transaction management)"""
    conn = get_db_connection()
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)  # Return results as dictionary
        yield cursor
        if commit:
            conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"⚠️ Transaction rolled back: {e}")
        raise
    finally:
        # Ensure resources are released
        if cursor:
            cursor.close()
        if conn.is_connected():
            conn.close()