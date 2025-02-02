from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Load app config (non-sensitive)
    app.config.from_object('app.config.AppConfig')
    
    # Initialize database module
    # init_database(app)
    
    # Register blueprints
    from .routes.health import health_bp
    from .routes.movies import movies_bp
    app.register_blueprint(health_bp)
    app.register_blueprint(movies_bp)
    
    return app