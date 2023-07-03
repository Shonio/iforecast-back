from app import db


class MeteoData(db.Model):
    __tablename__ = "meteo_data"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    power_plant_id = db.Column(
        db.Integer, db.ForeignKey("power_plants.id"), nullable=False
    )
    timestamp = db.Column(db.DateTime, nullable=False)
    temperature = db.Column(db.Numeric(10, 2), nullable=True)
    temperature_prediction = db.Column(db.Numeric(10, 2), nullable=False)
    irradiance = db.Column(db.Numeric(10, 2), nullable=True)
    irradiance_prediction = db.Column(db.Numeric(10, 2), nullable=False)
    cloudiness = db.Column(db.Numeric(10, 2), nullable=True)
    cloudiness_prediction = db.Column(db.Numeric(10, 2), nullable=False)
    wind_speed = db.Column(db.Numeric(10, 2), nullable=True)
    wind_speed_prediction = db.Column(db.Numeric(10, 2), nullable=False)
    precipitation = db.Column(db.Numeric(10, 2), nullable=True)
    precipitation_prediction = db.Column(db.Numeric(10, 2), nullable=False)

    power_plant = db.relationship("PowerPlant", back_populates="meteo_data")
