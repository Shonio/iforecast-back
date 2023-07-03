from datetime import timedelta
from typing import Dict

from flask_jwt_extended import create_access_token, create_refresh_token

from app.models.user import User


def user_data_response(user: User) -> Dict[str, Dict]:
    return {
        "user": user.serialize,
        "access_token": create_access_token(identity=user.id, expires_delta=timedelta(minutes=720)),
        "refresh_token": create_refresh_token(identity=user.id),
    }
