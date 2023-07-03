# Path: '.\app\models\plant_information.py
from app import db


class PlantInformation(db.Model):
    __tablename__ = "plant_information"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    power_plant_id = db.Column(
        db.Integer, db.ForeignKey("power_plants.id"), nullable=False
    )
    name = db.Column(db.String(255), nullable=False)
    value = db.Column(db.String(255), nullable=False)

    power_plant = db.relationship("PowerPlant", back_populates="plant_information")

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "value": self.value,
        }
