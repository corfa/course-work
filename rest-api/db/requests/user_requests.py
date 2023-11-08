from typing import Type

from sqlalchemy.orm import Session

from db.models import DBUsers
from db.exceptions.user_exception import DBUserNotFoundException, UsernameOrEmailAlreadyExists
from shemas.user import User


def create_user(db: Session, user: User, email_token: str) -> int:
    try:
        user_db = DBUsers(username=user.username, password=user.password, email=user.email, token=email_token)
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
        return user_db.id
    except:
        raise UsernameOrEmailAlreadyExists


def get_user_on_email(db: Session, email: str) -> DBUsers:
    user = db.query(DBUsers).filter(DBUsers.email == email).first()
    if user is None:
        raise DBUserNotFoundException()
    return user


def get_user_on_login(db: Session, login: str) -> DBUsers:
    user = db.query(DBUsers).filter(DBUsers.username == login).first()
    if user is None:
        raise DBUserNotFoundException()
    return user
