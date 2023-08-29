from datetime import datetime

from flask import Blueprint, jsonify, request
from flask.views import MethodView

from app.api.schemas import (PowerPlantDayStatsSchema, PowerPlantMonthStatsSchema, PowerPlantYearStatsSchema)
from app.api.services import power_plant_service

power_plant_bp = Blueprint("power_plant", __name__)

power_plant_day_data_schema = PowerPlantDayStatsSchema()
power_plant_month_data_schema = PowerPlantMonthStatsSchema()
power_plant_year_data_schema = PowerPlantYearStatsSchema()


class PowerPlantView(MethodView):
    # @jwt_required()
    def get_power_plant_day_stats(self):
        errors = power_plant_day_data_schema.validate(request.args)
        if errors:
            return jsonify(errors), 400

        power_plant_id = request.args.get("power_plant_id", type=int)
        timestamp = datetime.strptime(request.args.get("timestamp", type=str), "%Y-%m-%d").date()

        # ---------------------------------
        data = power_plant_service.get_power_plant_day_stats(power_plant_id, timestamp)
        # if data is empty, return 404
        if not data:
            return jsonify({"error": "Not found"}), 404
        # else, return data

        # Convert power and power_prediction to kWh and round to 3 decimal places
        # for d in data:
        #     if d.power is not None:
        #         d.power = round(float(d.power) / 1000, 3)
        #     if d.power_prediction is not None:
        #         d.power_prediction = round(float(d.power_prediction) / 1000, 3)

        return (jsonify({
            {"name": "Actual",
             "series": [{"name": d.timestamp.hour, "value": d.power, } for d in data],
             },
            {"name": "Prediction",
             "series": [{"name": d.timestamp.hour, "value": d.power_prediction, } for d in data],
             },
        }), 200,)

    def get_power_plant_monthly_stats(self):
        errors = power_plant_month_data_schema.validate(request.args)
        if errors:
            return jsonify(errors), 400

        power_plant_id = request.args.get("power_plant_id", type=int)
        timestamp = datetime.strptime(request.args.get("timestamp", type=str), "%Y-%m").date()

        # ---------------------------------
        data = power_plant_service.get_power_plant_monthly_stats(power_plant_id, timestamp)
        # if data is empty, return 404
        if not data:
            return jsonify({"error": "Not found"}), 404
        # else, return data
        return (jsonify(
            [{"labels": d.timestamp.day, "actual": d.total_power, "prediction": d.total_power_prediction, } for d in
                data]), 200,)

    def get_power_plant_yearly_stats(self):
        errors = power_plant_year_data_schema.validate(request.args)
        if errors:
            return jsonify(errors), 400

        power_plant_id = request.args.get("power_plant_id", type=int)
        timestamp = datetime.strptime(request.args.get("timestamp", type=str), "%Y").date()

        # ---------------------------------
        data = power_plant_service.get_power_plant_yearly_stats(power_plant_id, timestamp)
        # if data is empty, return 404
        if not data:
            return jsonify({"error": "Not found"}), 404
        # else, return data
        return (jsonify(
            [{"labels": d.timestamp.month, "actual": d.total_power, "prediction": d.total_power_prediction, } for d in
                data]), 200,)

    def dispatch_request(self, *args, **kwargs):
        if request.method == "GET":
            if request.path.endswith("day-stats"):
                return self.get_power_plant_day_stats()
            elif request.path.endswith("month-stats"):
                return self.get_power_plant_monthly_stats()
            elif request.path.endswith("year-stats"):
                return self.get_power_plant_yearly_stats()
        else:
            return jsonify({"error": "Method not allowed"}), 405


power_plant_view = PowerPlantView.as_view("power_plant_view")
power_plant_bp.add_url_rule("/api/v1/power-plant/day-stats", view_func=power_plant_view, methods=["GET"])
power_plant_bp.add_url_rule("/api/v1/power-plant/month-stats", view_func=power_plant_view, methods=["GET"])
power_plant_bp.add_url_rule("/api/v1/power-plant/year-stats", view_func=power_plant_view, methods=["GET"])
