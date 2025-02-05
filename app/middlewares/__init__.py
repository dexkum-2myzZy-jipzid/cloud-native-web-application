from .headers import apply_response_headers
from .auth import configure_auth_middleware

def register_middlewares(app):
    """Register all middlewares"""
    # Register auth middleware (before_request)
    configure_auth_middleware(app)
    
    # Register response headers middleware (after_request)
    app.after_request(apply_response_headers)