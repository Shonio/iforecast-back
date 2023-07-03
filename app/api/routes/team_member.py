from flask import Blueprint, jsonify, request, current_app
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.api.schemas import TeamMemberSchema, TeamMemberUpdateSchema
from app.api.services import user_service
from app.exceptions.handlers import CustomBadRequest

team_member_bp = Blueprint("team_member", __name__)
team_member_schema = TeamMemberSchema()
team_member_update_schema = TeamMemberUpdateSchema()


class TeamMemberView(MethodView):
    # @jwt_required()
    def delete(self, team_member_id):
        current_app.logger.info(request.headers)
        return jsonify({"message": f"Deleted team member {id}"}), 200
    #     print("JWT:", get_jwt_identity())
    #     ------------------------------------------------------------
    #     user_id = get_jwt_identity()
    #     if user_service.delete_team_member(user_id, team_member_id):
    #         return jsonify({"status": 200, "message": "Team member deleted"})
    #     else:
    #         raise CustomBadRequest("Team member deletion failed")
    #
    # @jwt_required()
    # def post(self):
    #     user_id = get_jwt_identity()
    #     errors = team_member_schema.validate(request.json)
    #     if errors:
    #         raise CustomBadRequest(description=jsonify(errors).get_data(as_text=True))
    #
    #     new_member = user_service.add_team_member(user_id, **request.json)
    #     if new_member:
    #         return jsonify(new_member.serialize), 201
    #     else:
    #         raise CustomBadRequest("Team member addition failed")

    @jwt_required()
    def patch(self):
        user_id = get_jwt_identity()
        errors = team_member_update_schema.validate(request.json)
        if errors:
            raise CustomBadRequest(description=jsonify(errors).get_data(as_text=True))

        if user_service.update_team_member(user_id, request.json["id"], **request.json):
            return jsonify({"status": 200, "message": "Team member updated"}), 200
        else:
            raise CustomBadRequest("Team member update failed")


team_member_view = TeamMemberView.as_view("team_member_view")
team_member_bp.add_url_rule(
    "/api/team_member/<int:team_member_id>",
    view_func=team_member_view,
    methods=["DELETE"],
)
team_member_bp.add_url_rule(
    "/api/team_member", view_func=team_member_view, methods=["POST"]
)
team_member_bp.add_url_rule(
    "/api/team_member", view_func=team_member_view, methods=["PATCH"]
)
