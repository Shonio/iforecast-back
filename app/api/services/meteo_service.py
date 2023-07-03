# Path: '.\app\api\services\power_plant_service.py'
from datetime import date, timedelta
from typing import List, Optional

from app.models import MeteoData


def get_meteo_day_stats(power_plant_id: int, day: date) -> Optional[List[MeteoData]]:
    return (
        MeteoData.query.filter_by(power_plant_id=power_plant_id)
        .filter(MeteoData.timestamp >= day)
        .filter(MeteoData.timestamp < day + timedelta(days=1))
        .all()
    )
