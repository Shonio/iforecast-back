from datetime import datetime

from flask import Blueprint, jsonify, request
from flask.views import MethodView

from app.api.schemas import (PowerPlantDayStatsSchema, PowerPlantMonthStatsSchema, PowerPlantYearStatsSchema,
                             PowerPlantDayStatsRangeSchema)
from app.api.services import power_plant_service

power_plant_bp = Blueprint("power_plant", __name__)

power_plant_day_data_schema = PowerPlantDayStatsSchema()
power_plant_day_data_range_schema = PowerPlantDayStatsRangeSchema()
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

        plant_prediction_models = power_plant_service.get_prediction_models_by_power_plant_id(power_plant_id)

        # Check if there is any prediction model
        if plant_prediction_models.empty:
            return jsonify({"error": "Not found"}), 404

        # Get prediction models ids
        model_ids = plant_prediction_models["id"].tolist()

        # Get power plant stats with model data
        data = power_plant_service.get_power_plant_stats_with_model_data(power_plant_id, timestamp, model_ids)

        # Check if there is any data
        if data.empty:
            return jsonify({"error": "Not found"}), 404

        # Get unique model ids
        model_ids = data["prediction_model_id"].unique().tolist()

        # Build response
        response = []
        actual_data = data[data["prediction_model_id"] == model_ids[0]]
        response.append({
            "name": "Actual",
            "series": [{"name": d.timestamp.hour, "value": d.power, } for d in actual_data.itertuples()],
        })

        # Get prediction models data
        for model_id in model_ids:
            model_data = data[data["prediction_model_id"] == model_id]
            response.append({
                "name": plant_prediction_models[plant_prediction_models["id"] == model_id]["name"].values[0],
                "series": [{"name": d.timestamp.hour, "value": d.power_prediction, } for d in model_data.itertuples()],
            })

        return jsonify(response), 200


    def get_power_plant_day_stats_range(self):
        errors = power_plant_day_data_range_schema.validate(request.args)
        if errors:
            return jsonify(errors), 400

        power_plant_id = request.args.get("power_plant_id", type=int)
        start_date = datetime.strptime(request.args.get("startDate", type=str), "%Y-%m-%d").date()
        end_date = datetime.strptime(request.args.get("endDate", type=str), "%Y-%m-%d").date()

        plant_prediction_models = power_plant_service.get_prediction_models_by_power_plant_id(power_plant_id)

        # Check if there is any prediction model
        if plant_prediction_models.empty:
            return jsonify({"error": "Not found"}), 404

        # Get prediction models ids
        model_ids = plant_prediction_models["id"].tolist()

        # Get power plant stats with model data
        data = power_plant_service.get_power_plant_stats_in_range_with_model_data(power_plant_id, start_date, end_date, model_ids)

        # Format data timestamp to match 'YYYY-MM-DD HH' format
        data["dt"] = data["timestamp"].dt.strftime("%Y-%m-%d")

        # Check if there is any data
        if data.empty:
            return jsonify({"error": "Not found"}), 404

        # Get unique model ids
        model_ids = data["prediction_model_id"].unique().tolist()

        # Build response
        response = []
        actual_data = data[data["prediction_model_id"] == model_ids[0]]

        # Get unique dt with format 'YYYY-MM-DD'
        unique_dt = actual_data["dt"].unique().tolist()

        # Generate series for each unique dt
        series = []
        for dt in unique_dt:
            series.append({"dt": dt, "data": [{"name": d.timestamp.hour, "value": d.power, } for d in actual_data[actual_data["dt"] == dt].itertuples()]})

        response.append({
            "name": "Actual",
            "series": series,
        })

        # Get prediction models data
        for model_id in model_ids:
            model_data = data[data["prediction_model_id"] == model_id]
            # Get series for each unique dt
            series = []
            for dt in unique_dt:
                series.append({"dt": dt, "data": [{"name": d.timestamp.hour, "value": d.power_prediction, } for d in model_data[model_data["dt"] == dt].itertuples()]})

            response.append({
                "name": plant_prediction_models[plant_prediction_models["id"] == model_id]["name"].values[0],
                "series": series,
            })

        return jsonify(response), 200


    def get_power_plant_monthly_stats(self):
        errors = power_plant_month_data_schema.validate(request.args)
        if errors:
            return jsonify(errors), 400

        power_plant_id = request.args.get("power_plant_id", type=int)
        timestamp = datetime.strptime(request.args.get("timestamp", type=str), "%Y-%m").date()

        plant_prediction_models = power_plant_service.get_prediction_models_by_power_plant_id(power_plant_id)

        # Check if there is any prediction model
        if plant_prediction_models.empty:
            return jsonify({"error": "Not found"}), 404

        # Get prediction models ids
        model_ids = plant_prediction_models["id"].tolist()

        # Get power plant stats with model data
        data = power_plant_service.get_monthly_stats_with_model_data(power_plant_id, timestamp, model_ids)

        # Check if there is any data
        if data.empty:
            return jsonify({"error": "Not found"}), 404

        # Get unique model ids
        model_ids = data["prediction_model_id"].unique().tolist()

        # Build response
        response = []
        actual_data = data[data["prediction_model_id"] == model_ids[0]]
        response.append({
            "name": "Actual",
            "series": [{"name": d.timestamp.day, "value": d.total_power, } for d in actual_data.itertuples()],
        })

        # Get prediction models data
        for model_id in model_ids:
            model_data = data[data["prediction_model_id"] == model_id]
            response.append({
                "name": plant_prediction_models[plant_prediction_models["id"] == model_id]["name"].values[0],
                "series": [{"name": d.timestamp.day, "value": d.total_power_prediction, } for d in model_data.itertuples()],
            })

        return jsonify(response), 200

    def get_power_plant_yearly_stats(self):
        errors = power_plant_year_data_schema.validate(request.args)
        if errors:
            return jsonify(errors), 400

        power_plant_id = request.args.get("power_plant_id", type=int)
        timestamp = datetime.strptime(request.args.get("timestamp", type=str), "%Y").date()

        plant_prediction_models = power_plant_service.get_prediction_models_by_power_plant_id(power_plant_id)

        # Check if there is any prediction model
        if plant_prediction_models.empty:
            return jsonify({"error": "Not found"}), 404

        # Get prediction models ids
        model_ids = plant_prediction_models["id"].tolist()

        # Get power plant stats with model data
        data = power_plant_service.get_yearly_stats_with_model_data(power_plant_id, timestamp, model_ids)

        # Check if there is any data
        if data.empty:
            return jsonify({"error": "Not found"}), 404

        # Get unique model ids
        model_ids = data["prediction_model_id"].unique().tolist()

        # Build response
        response = []
        actual_data = data[data["prediction_model_id"] == model_ids[0]]
        response.append({
            "name": "Actual",
            "series": [{"name": d.timestamp.month, "value": d.total_power, } for d in actual_data.itertuples()],
        })

        # Get prediction models data
        for model_id in model_ids:
            model_data = data[data["prediction_model_id"] == model_id]
            response.append({
                "name": plant_prediction_models[plant_prediction_models["id"] == model_id]["name"].values[0],
                "series": [{"name": d.timestamp.month, "value": d.total_power_prediction, } for d in model_data.itertuples()],
            })

        return jsonify(response), 200


    def dispatch_request(self, *args, **kwargs):
        if request.method == "GET":
            if request.path.endswith("day-stats"):
                return self.get_power_plant_day_stats()
            elif request.path.endswith("month-stats"):
                return self.get_power_plant_monthly_stats()
            elif request.path.endswith("day-stats-range"):
                return self.get_power_plant_day_stats_range()
            elif request.path.endswith("year-stats"):
                return self.get_power_plant_yearly_stats()
        else:
            return jsonify({"error": "Method not allowed"}), 405


power_plant_view = PowerPlantView.as_view("power_plant_view")
power_plant_bp.add_url_rule("/api/v1/power-plant/day-stats", view_func=power_plant_view, methods=["GET"])
power_plant_bp.add_url_rule("/api/v1/power-plant/day-stats-range", view_func=power_plant_view, methods=["GET"])
power_plant_bp.add_url_rule("/api/v1/power-plant/month-stats", view_func=power_plant_view, methods=["GET"])
power_plant_bp.add_url_rule("/api/v1/power-plant/year-stats", view_func=power_plant_view, methods=["GET"])
