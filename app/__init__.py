from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


database = SQLAlchemy()
Jwt = JWTManager()
migrate = Migrate()

def auth_app():

    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Init extensions
    database.init_app(app)
    Jwt.init_app(app)
    migrate.init_app(app, database)
    from .models import user

    # Register blueprints
    from app.routes.auth_routes import auth_bp
    # from app.routes.user_routes import user_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    # app.register_blueprint(user_bp, url_prefix="/user")

    return app


