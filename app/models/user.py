from app import bcrypt, db
from app.models.power_plant import PowerPlant


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum("admin", "user", "guest"), nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    updated = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum("active", "inactive", "suspended"), nullable=False)

    power_plants = db.relationship("PowerPlant", back_populates="user", lazy=False)
    team_members = db.relationship("TeamMember", back_populates="user", lazy=False)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def has_power_plant(self, power_plant_id: int) -> bool:
        power_plant = PowerPlant.query.filter_by(
            id=power_plant_id, user_id=self.id
        ).first()
        return power_plant is not None

    @property
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "role": self.role,
            "created": str(self.created),
            "updated": str(self.updated),
            "status": self.status,
            "power_plants": [pp.serialize for pp in self.power_plants],
            "team_members": [tm.serialize for tm in self.team_members],
        }
