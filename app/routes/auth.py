import mysql.connector
import hashlib
import os
import jwt
import datetime
from flask import Blueprint, request, jsonify, current_app
from database.connection import get_db_connection

auth_bp = Blueprint("auth", __name__, url_prefix="/v1")

def hash_password(password):
    salt = os.urandom(16).hex()
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}${hashed}"

def verify_password(stored_password, provided_password):
    try:
        salt, hashed = stored_password.split("$")
        return hashlib.sha256((salt + provided_password).encode()).hexdigest() == hashed
    except ValueError:
        return False

@auth_bp.route("/register", methods=["POST"])
def register():
    conn = None
    try:
        data = request.get_json()
        if not data or "email" not in data or "password" not in data:
            return jsonify({"error": "Missing email or password"}), 400

        email = data["email"].strip()
        password = data["password"].strip()

        if not email or not password:
            return jsonify({"error": "Email and password cannot be empty"}), 400

        hashed_password = hash_password(password)

        conn = get_db_connection()
        if conn is None or not conn.is_connected():
            return jsonify({"error": "Service Unavailable"}), 503

        with conn.cursor() as cursor:
            try:
                cursor.execute(
                    "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
                    (email, hashed_password)
                )
                conn.commit()
            except mysql.connector.IntegrityError:
                return jsonify({"error": "Email already registered"}), 400

        return jsonify({}), 201

    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()

@auth_bp.route("/login", methods=["POST"])
def login():
    conn = None
    try:
        data = request.get_json()
        if not data or "email" not in data or "password" not in data:
            return jsonify({"error": "Missing email or password"}), 400

        email = data["email"].strip()
        password = data["password"].strip()

        conn = get_db_connection()
        if conn is None or not conn.is_connected():
            return jsonify({"error": "Service Unavailable"}), 503

        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT id, password_hash FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

        if not user or not verify_password(user["password_hash"], password):
            return jsonify({"error": "Invalid email or password"}), 400

        secret_key = current_app.config["SECRET_KEY"]
        jwt_algorithm = current_app.config.get("JWT_ALGORITHM", "HS256")
        jwt_expiration_hours = current_app.config.get("JWT_EXPIRATION_HOURS", 24)

        token = jwt.encode(
            {
                "user_id": user["id"],
                "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=jwt_expiration_hours),
            },
            secret_key,
            algorithm=jwt_algorithm
        )

        return jsonify({"token": token}), 200

    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()