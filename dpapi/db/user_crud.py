from sqlalchemy.orm import Session

from dpapi.db import models
from dpapi.schema.login import UserInDB


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def save_user(db: Session, user: UserInDB):
    db_user = models.User(full_name=user.full_name,
                          email=user.email,
                          hashed_password=user.hashed_password,
                          disabled=user.disabled)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
