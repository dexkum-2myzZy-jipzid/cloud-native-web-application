import os
from dotenv import load_dotenv

# load_dotenv()
class AppConfig:
    # SECRET_KEY = os.getenv('FLASK_SECRET', 'default-secret-key')
    JSON_SORT_KEYS = False 
    JSONIFY_PRETTYPRINT_REGULAR = False