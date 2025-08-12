import redis
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .config import Config

database = SQLAlchemy()
Jwt = JWTManager()
migrate = Migrate()
redis_client=redis.StrictRedis.from_url(Config.REDIS_URL,decode_responses=True)