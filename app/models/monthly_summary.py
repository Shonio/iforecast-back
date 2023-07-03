from app import db


class MonthlySummary(db.Model):
    __tablename__ = "monthly_summary"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    power_plant_id = db.Column(
        db.Integer, db.ForeignKey("power_plants.id"), nullable=False
    )
    timestamp = db.Column(db.Date, nullable=False)
    total_power = db.Column(db.Numeric(10, 0), nullable=False)
    total_power_prediction = db.Column(db.Numeric(10, 0), nullable=False)

    power_plant = db.relationship("PowerPlant", back_populates="monthly_summaries")

    def __repr__(self):
        return f"MonthlySummary(id={self.id}, power_plant_id={self.power_plant_id}, year={self.year}, month={self.month}, total_power={self.total_power})"
