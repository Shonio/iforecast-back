from app import db


class PlantData(db.Model):
    __tablename__ = "plant_data"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    power_plant_id = db.Column(
        db.Integer, db.ForeignKey("power_plants.id"), nullable=False
    )
    timestamp = db.Column(db.DateTime, nullable=False)
    power = db.Column(db.Numeric(10, 2), nullable=True)
    power_prediction = db.Column(db.Numeric(10, 2), nullable=False)

    power_plant = db.relationship("PowerPlant", back_populates="plant_data")

    def __repr__(self):
        return f"PlantData(id={self.id}, power_plant_id={self.power_plant_id}, timestamp='{self.timestamp}', power={self.power}, power_prediction={self.power_prediction})"
