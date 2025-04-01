from flask import Flask
from app.config import AppConfig
from app.middlewares import register_middlewares
from app.routes.health import health_bp
from app.routes.movies import movies_bp
from app.routes.links import links_bp
from app.routes.ratings import ratings_bp
from app.routes.auth import auth_bp
from app.routes.metadata import metadata_bp


def create_app():
    # Create Flask app
    app = Flask(__name__)

    # Load config
    app.config.from_object(AppConfig)

    # Register middleware
    register_middlewares(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(movies_bp)
    app.register_blueprint(links_bp)
    app.register_blueprint(ratings_bp)
    app.register_blueprint(metadata_bp)

    # Global error handling
    # @app.errorhandler(404)
    @app.errorhandler(405)
    def handle_unsupported(e):
        return {"error": "Bad Request"}, 400

    # Debugging
    # print(app.url_map)

    return app
