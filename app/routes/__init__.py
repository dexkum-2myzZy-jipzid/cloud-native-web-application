from .health import health_bp
from .movies import movies_bp
from .links import links_bp
from .ratings import ratings_bp
from .auth import auth_bp
from .metadata import metadata_bp

__all__ = ["auth_bp", "health_bp", "movies_bp", "links_bp", "ratings_bp", "metadata_bp"]
