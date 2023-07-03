from urllib.parse import urlparse

from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy

from config import Config

bcrypt = Bcrypt()
db = SQLAlchemy()
jwt = JWTManager()
cors = CORS(resources={r"/api/*": {"origins": "*"}})
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=urlparse(f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}").geturl(),
)
