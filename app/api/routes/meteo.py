from datetime import datetime

from flask import Blueprint, jsonify, request
from flask.views import MethodView

from app.api.schemas import MeteoDayStatsSchema
from app.api.services import meteo_service

meteo_bp = Blueprint("meteo", __name__)
meteo_day_data_schema = MeteoDayStatsSchema()


class MeteoView(MethodView):
    # @jwt_required()
    def get_meteo_day_stats(self):
        errors = meteo_day_data_schema.validate(request.args)
        if errors:
            return jsonify(errors), 400

        power_plant_id = request.args.get("power_plant_id", type=int)
        timestamp = datetime.strptime(
            request.args.get("timestamp", type=str), "%Y-%m-%d"
        ).date()

        # ---------------------------------
        data = meteo_service.get_meteo_day_stats(power_plant_id, timestamp)
        # if data is empty, return 404
        if not data:
            return jsonify({"error": "Not found"}), 404
        # else, return data
        return (
            jsonify(
                [
                    {
                        "labels": d.timestamp.hour,
                        "temperature": {
                            "actual": d.temperature,
                            "prediction": d.temperature_prediction,
                        },
                        "irradiance": {
                            "actual": d.irradiance,
                            "prediction": d.irradiance_prediction,
                        },
                        "cloudiness": {
                            "actual": d.cloudiness,
                            "prediction": d.cloudiness_prediction,
                        },
                        "wind_speed": {
                            "actual": d.wind_speed,
                            "prediction": d.wind_speed_prediction,
                        },
                        "precipitation": {
                            "actual": d.precipitation,
                            "prediction": d.precipitation_prediction,
                        },
                    }
                    for d in data
                ]
            ),
            200,
        )

    # ---------------------------------

    def dispatch_request(self, *args, **kwargs):
        if request.method == "GET":
            if request.path.endswith("day-stats"):
                return self.get_meteo_day_stats()
        else:
            return jsonify({"error": "Method not allowed"}), 405


power_plant_view = MeteoView.as_view("power_plant_view")
meteo_bp.add_url_rule(
    "/api/v1/meteo/day-stats", view_func=power_plant_view, methods=["GET"]
)
