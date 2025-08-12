from flask import Flask
from .extension import database, Jwt, migrate, redis_client


def auth_app(config_class: str = "app.config.Config") -> Flask:
    """
    Application factory function for creating a Flask app instance.

    Args:
        config_class (str): Path to the configuration class.

    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config_class)

    # Initialize extensions
    _register_extensions(app)

    # Register blueprints
    _register_blueprints(app)

    # Run optional service health checks
    _check_redis_connection()

    return app


def _register_extensions(app: Flask) -> None:
    """Initialize Flask extensions."""
    database.init_app(app)
    Jwt.init_app(app)
    migrate.init_app(app, database)


def _register_blueprints(app: Flask) -> None:
    """Register Flask blueprints."""
    from app.routes.auth_routes import auth_bp
    # from app.routes.user_routes import user_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    # app.register_blueprint(user_bp, url_prefix="/user")


def _check_redis_connection() -> None:
    """Ping Redis and log status (non-blocking for production)."""
    try:
        redis_client.ping()
        print("✅ Redis connected successfully")
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
