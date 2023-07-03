# Path: '.\app\api\services\power_plant_service.py'
from datetime import date, timedelta
from typing import List, Optional

from sqlalchemy import extract

from app.models import MonthlySummary, PlantData, YearlySummary


def get_power_plant_day_stats(
    power_plant_id: int, day: date
) -> Optional[List[PlantData]]:
    return (
        PlantData.query.filter_by(power_plant_id=power_plant_id)
        .filter(PlantData.timestamp >= day)
        .filter(PlantData.timestamp < day + timedelta(days=1))
        .all()
    )


def get_power_plant_monthly_stats(
    power_plant_id: int, month: date
) -> Optional[List[MonthlySummary]]:
    return (
        MonthlySummary.query.filter_by(power_plant_id=power_plant_id)
        .filter(extract("year", MonthlySummary.timestamp) == month.year)
        .filter(extract("month", MonthlySummary.timestamp) == month.month)
        .order_by(MonthlySummary.timestamp)
        .all()
    )


def get_power_plant_yearly_stats(
    power_plant_id: int, year: date
) -> Optional[List[YearlySummary]]:
    return (
        YearlySummary.query.filter_by(power_plant_id=power_plant_id)
        .filter(extract("year", YearlySummary.timestamp) == year.year)
        .order_by(YearlySummary.timestamp)
        .all()
    )
