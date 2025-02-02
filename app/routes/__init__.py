from flask import Flask
from app.config import AppConfig
from app.middlewares.headers import apply_response_headers
from app.routes.health import health_bp
from app.routes.movies import movies_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(AppConfig)
    
    # Register middleware
    app.after_request(apply_response_headers)
    
    # Register blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(movies_bp)
    
    # Error handling
    @app.errorhandler(404)
    @app.errorhandler(405)
    def handle_unsupported(e):
        return {"error": "Bad Request"}, 400
    
    return app