import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from flask import Flask

from app.exceptions.handlers import CustomBadRequest, handle_error
from app.exceptions.handlers import init_app as init_error_handlers
from app.extensions import bcrypt, cors, db, jwt, limiter
from config import Config


def create_app(config_class=Config):
    from app.api.routes.auth import auth_bp
    from app.api.routes.meteo import meteo_bp
    from app.api.routes.power_plant import power_plant_bp
    from app.api.routes.team_member import team_member_bp
    from app.api.routes.user import user_bp

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Logging configuration
    configure_logging(app)

    # Error handlers registration
    register_error_handlers(app)

    # Extensions initialization
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    limiter.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(power_plant_bp)
    app.register_blueprint(meteo_bp)
    app.register_blueprint(team_member_bp)
    app.register_blueprint(user_bp)

    return app


def configure_logging(app):
    if not app.debug:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        file_handler = RotatingFileHandler(
            log_dir / "app.log", maxBytes=10240, backupCount=10
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
            )
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("App startup")


def register_error_handlers(app):
    app.errorhandler(CustomBadRequest)(handle_error(400))
