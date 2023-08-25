from flask import Blueprint, current_app, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                jwt_required)

from app.api.routes.utils import user_data_response
from app.api.schemas import LoginSchema
from app.api.services import user_service
from app.exceptions.handlers import CustomBadRequest, handle_error

auth_bp = Blueprint("auth", __name__)

login_schema = LoginSchema()


class AuthView(MethodView):
    @jwt_required()
    def access_token(self):
        access_token = request.json.get("access_token", None)
        if access_token:
            user_id = get_jwt_identity()
            user = user_service.get_user_by_id(user_id)

            if user:
                return jsonify(user_data_response(user))
            else:
                current_app.logger.error("User not found with user_id: %s", user_id)
                return handle_error("User not found", 404)
        else:
            current_app.logger.error("Access token not found in request")
            return handle_error("Access token not found", 404)

    @jwt_required(refresh=True)
    def refresh(self):
        user_id = get_jwt_identity()
        new_access_token = create_access_token(identity=user_id)

        return jsonify({"access_token": new_access_token})

    def sign_in(self):
        errors = login_schema.validate(request.json)
        if errors:
            raise CustomBadRequest(description=jsonify(errors).get_data(as_text=True))

        email = request.json.get("email", None)
        password = request.json.get("password", None)

        user = user_service.get_user_by_email(email)
        if user and user.check_password(password):
            return jsonify(user_data_response(user)), 200
        else:
            return handle_error("Invalid email or password", 403)

    def dispatch_request(self, *args, **kwargs):
        if request.path.endswith("access-token"):
            return self.access_token()
        elif request.path.endswith("refresh"):
            return self.refresh()
        elif request.path.endswith("sign-in"):
            return self.sign_in()
        else:
            return jsonify({"error": "Request not allowed"}), 405


auth_view = AuthView.as_view("auth_view")
auth_bp.add_url_rule("/api/auth/access-token", view_func=auth_view, methods=["POST"])
auth_bp.add_url_rule("/api/auth/refresh", view_func=auth_view, methods=["POST"])
auth_bp.add_url_rule("/api/auth/sign-in", view_func=auth_view, methods=["POST"])
