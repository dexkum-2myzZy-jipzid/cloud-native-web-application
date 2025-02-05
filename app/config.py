import os
from dotenv import load_dotenv

# load_dotenv()
class AppConfig:
    SECRET_KEY = os.getenv('FLASK_SECRET', 'default-secret-key')
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRATION_HOURS = 24 * 7 # 1 week
    # JSON_SORT_KEYS = False 
    # JSONIFY_PRETTYPRINT_REGULAR = False