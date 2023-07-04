from typing import Optional

from app import db
from app.models import TeamMember, User


def get_user_by_email(email: str) -> Optional[User]:
    return User.query.filter_by(email=email).first()


def get_user_by_id(user_id: int) -> Optional[User]:
    return User.query.filter_by(id=user_id).first()


def get_all_team_members(user_id: int) -> Optional[TeamMember]:
    user = get_user_by_id(user_id)
    if user:
        return TeamMember.query.filter_by(user_id=user_id).all()
    return None


def update_team_member(user_id: int, team_member_id: int, **kwargs) -> bool:
    user = get_user_by_id(user_id)
    if user:
        team_member = TeamMember.query.get(team_member_id)
        if team_member and team_member.user_id == user_id:
            for key, value in kwargs.items():
                if hasattr(team_member, key):
                    setattr(team_member, key, value)

            db.session.commit()
            return True
    return False


def delete_team_member(user_id: int, team_member_id: int) -> bool:
    user = get_user_by_id(user_id)
    if user:
        team_member = TeamMember.query.get(team_member_id)
        if team_member and team_member.user_id == user_id:
            db.session.delete(team_member)
            db.session.commit()
            return True
    return False


def add_team_member(
    user_id: int, full_name: str, position: str, phone: int
) -> Optional[TeamMember]:
    user = get_user_by_id(user_id)
    if user:
        new_team_member = TeamMember(
            user_id=user_id, full_name=full_name, position=position, phone=phone
        )
        db.session.add(new_team_member)
        db.session.commit()

        return new_team_member
    return None


def change_email(user_id: int, new_email: str, password: str) -> bool:
    user = get_user_by_id(user_id)
    if user and user.check_password(password):
        if not get_user_by_email(new_email):  # Check if new email already exists
            user.email = new_email
            db.session.commit()
            return True
    return False


def change_password(user_id: int, current_password: str, new_password: str) -> bool:
    user = get_user_by_id(user_id)
    if user and user.check_password(current_password):
        user.set_password(new_password)
        db.session.commit()
        return True
    return False
