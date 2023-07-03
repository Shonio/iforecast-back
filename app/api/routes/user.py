from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.api.schemas import ChangeEmailSchema, ChangePasswordSchema
from app.api.services import user_service
from app.exceptions.handlers import CustomBadRequest

user_bp = Blueprint("user", __name__)
change_email_schema = ChangeEmailSchema()
change_password_schema = ChangePasswordSchema()


class UserView(MethodView):
    @jwt_required()
    def patch(self):
        user_id = get_jwt_identity()
        if request.path.endswith("email"):
            errors = change_email_schema.validate(request.json)
            if errors:
                raise CustomBadRequest(
                    description=jsonify(errors).get_data(as_text=True)
                )
            if user_service.change_email(user_id, **request.json):
                return jsonify({"message": "Email changed"}), 200
            else:
                raise CustomBadRequest("Email change failed")
        elif request.path.endswith("password"):
            errors = change_password_schema.validate(request.json)
            if errors:
                raise CustomBadRequest(
                    description=jsonify(errors).get_data(as_text=True)
                )
            if user_service.change_password(user_id, **request.json):
                return jsonify({"message": "Password changed"}), 200
            else:
                raise CustomBadRequest("Password change failed")


user_view = UserView.as_view("user_view")
user_bp.add_url_rule("/api/user/email", view_func=user_view, methods=["PATCH"])
user_bp.add_url_rule("/api/user/password", view_func=user_view, methods=["PATCH"])
