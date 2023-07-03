# Path: '.\app\models\team_member.py
from app import db


class TeamMember(db.Model):
    __tablename__ = "team_members"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    position = db.Column(
        db.Enum("Director", "Engineer", "Operator", "Dispatcher"), nullable=False
    )
    phone = db.Column(db.BigInteger, nullable=False)

    user = db.relationship("User", back_populates="team_members")

    @property
    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "position": self.position,
            "phone": self.phone,
        }
