from app import db


class PowerPlant(db.Model):
    __tablename__ = "power_plants"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Enum("SPP", "WPP"), nullable=False)
    tariff = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    user = db.relationship("User", back_populates="power_plants")
    plant_information = db.relationship(
        "PlantInformation", back_populates="power_plant", lazy=False
    )

    meteo_data = db.relationship("MeteoData", back_populates="power_plant", lazy=True)
    plant_data = db.relationship("PlantData", back_populates="power_plant", lazy=True)
    yearly_summaries = db.relationship(
        "YearlySummary", back_populates="power_plant", lazy=True
    )
    monthly_summaries = db.relationship(
        "MonthlySummary", back_populates="power_plant", lazy=True
    )

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "tariff": self.tariff,
            "capacity": self.capacity,
            "plant_information": [info.serialize for info in self.plant_information],
        }
