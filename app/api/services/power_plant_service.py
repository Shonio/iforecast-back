# Path: '.\app\api\services\power_plant_service.py'
from datetime import date, timedelta
from typing import List, Optional
import pandas as pd

from sqlalchemy import extract
from sqlalchemy import text

from app.models import MonthlySummary, PlantData, YearlySummary
from app.extensions import db


def get_prediction_models_by_power_plant_id(power_plant_id: int) -> pd.DataFrame:
    sql_query = text("SELECT id, name FROM prediction_models WHERE power_plant_id = :power_plant_id AND is_active = 1;")
    result = db.session.execute(sql_query, {'power_plant_id': power_plant_id})
    df = pd.DataFrame(result.fetchall())
    df.columns = result.keys()  # set DataFrame columns to match SQL query result
    return df


def get_yearly_stats_with_model_data(power_plant_id: int, timestamp: date, model_ids: list) -> pd.DataFrame:
    # Get data for year of timestamp
    # SELECT * FROM yearly_summary as ys INNER JOIN yearly_summary_predictions as ysp ON ysp.yearly_summary_id=ys.id where ys.power_plant_id = 1 and ys.timestamp >= '2023-01-01' and ys.timestamp < '2024-01-01' and ysp.prediction_model_id in (1, 2);
    sql_query = text(
        f"SELECT * FROM yearly_summary as ys INNER JOIN yearly_summary_predictions as ysp ON ysp.yearly_summary_id=ys.id where ys.power_plant_id = :power_plant_id and ys.timestamp >= :start_date and ys.timestamp < :end_date and ysp.prediction_model_id in :model_ids;")

    # Calculate start and end date for query
    start_date = timestamp.replace(month=1, day=1)
    end_date = start_date + timedelta(days=366)
    end_date = end_date.replace(month=1, day=1)

    result = db.session.execute(sql_query,
                                {'power_plant_id': power_plant_id, 'start_date': start_date, 'end_date': end_date,
                                 'model_ids': tuple(model_ids)})
    df = pd.DataFrame(result.fetchall())

    # If df is empty, return empty df
    if df.empty:
        return df
    else:
        df.columns = result.keys()
        return df


def get_monthly_stats_with_model_data(power_plant_id: int, timestamp: date, model_ids: list) -> pd.DataFrame:
    # Get data for month and year of timestamp
    # SELECT * FROM monthly_summary as ms INNER JOIN monthly_summary_predictions as msp ON msp.monthly_summary_id=ms.id where ms.power_plant_id = 1 and ms.timestamp >= '2023-08-01' and ms.timestamp < '2023-09-01'and msp.prediction_model_id in (1, 2);
    sql_query = text(
        f"SELECT * FROM monthly_summary as ms INNER JOIN monthly_summary_predictions as msp ON msp.monthly_summary_id=ms.id where ms.power_plant_id = :power_plant_id and ms.timestamp >= :start_date and ms.timestamp < :end_date and msp.prediction_model_id in :model_ids;")

    # Calculate start and end date for query
    start_date = timestamp.replace(day=1)
    end_date = start_date + timedelta(days=32)
    end_date = end_date.replace(day=1)

    result = db.session.execute(sql_query,
                                {'power_plant_id': power_plant_id, 'start_date': start_date, 'end_date': end_date,
                                 'model_ids': tuple(model_ids)})
    df = pd.DataFrame(result.fetchall())
    # If df is empty, return empty df
    if df.empty:
        return df
    else:
        df.columns = result.keys()  # set DataFrame columns to match SQL query result
        return df


def get_power_plant_stats_with_model_data(power_plant_id: int, timestamp: date, model_ids: list) -> pd.DataFrame:
    # SELECT * FROM solar_power_system.plant_data as pd INNER JOIN plant_data_predictions as pdp ON pdp.plant_data_id=pd.id where pd.timestamp >= '2023-08-25' and  pd.timestamp < '2023-08-26' and pdp.prediction_model_id in (1, 2)
    sql_query = text(f"SELECT * FROM plant_data as pd INNER JOIN plant_data_predictions as pdp ON pdp.plant_data_id=pd.id where pd.power_plant_id = {power_plant_id} and pd.timestamp >= '{timestamp}' and  pd.timestamp < '{timestamp + timedelta(days=1)}' and pdp.prediction_model_id in ({', '.join(map(str, model_ids))});")
    result = db.session.execute(sql_query)
    df = pd.DataFrame(result.fetchall())

    # If df is empty, return empty df
    if df.empty:
        return df
    else:
        df.columns = result.keys()
        return df


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
