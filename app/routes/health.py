from flask import Blueprint, request
from database.connection import get_db_connection

health_bp = Blueprint('health', __name__, url_prefix='/v1')

@health_bp.route('/healthcheck', methods=['GET'])
def healthcheck():
    if request.args or request.form:
        return {"error": "Bad Request"}, 400
    
    try:
        conn = get_db_connection()
        if conn and conn.is_connected():
            conn.close()
            return {"status": "OK"}, 200
        return {"error": "Service Unavailable"}, 503
    except Exception:
        return {"error": "Service Unavailable"}, 503