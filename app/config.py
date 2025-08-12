import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    #REDIS_DATABASE_CONFIGURATION
    REDIS_URL=os.environ.get("REDIS_URL")
    REFRESH_TOKEN_SECRET=os.environ.get("REFRESH_TOKEN_SECRET")
    REFRESH_TOKEN_TTL=int (os.environ.get("REFRESH_TOKEN_TTL"))

class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
