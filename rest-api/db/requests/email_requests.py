from sqlalchemy.orm import Session

from db.models import DBUsers


def confirm_email(db: Session,email):
    user = db.query(DBUsers).filter(DBUsers.email == email).first()
    user.confirmed = True
    db.commit()
