import os
import secrets
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class Config:
    LOGIN_RATE_LIMIT = os.getenv("LOGIN_RATE_LIMIT", "5 per minute")
    REFRESH_RATE_LIMIT = os.getenv("REFRESH_RATE_LIMIT", "10 per hour")
    SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", secrets.token_urlsafe(32))
    JWT_TOKEN_LOCATION = ["headers"]
    REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES", 120))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.environ.get("JWT_REFRESH_TOKEN_EXPIRES", 30))
    )
