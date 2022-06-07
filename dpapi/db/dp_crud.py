from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import and_

from dpapi.db import models
from dpapi.schema.dp_api import ScriptInDB


def create_script(db: Session, script: ScriptInDB):
    db_script = models.Script(name=script.name,
                              content=script.content,
                              note=script.note,
                              created=script.created,
                              user_id=script.user_id)
    db.add(db_script)
    db.commit()
    db.refresh(db_script)
    return db_script


def get_script(db: Session, userid: str):
    return db.query(models.Script).filter_by(user_id=userid).order_by(models.Script.name).all()


def update_script(db: Session, script: ScriptInDB):
    db_script = db.query(models.Script)\
        .filter(and_(models.Script.id == script.script_id, models.Script.user_id == script.user_id)).first()
    if db_script:
        db_script.name = script.name
        db_script.content = script.content
        db_script.note = script.note
        db_script.updated = script.updated
        db.commit()
        db.refresh(db_script)
    return db_script


def delete_script(db: Session, script_id: str, userid: str):
    db.query(models.Script).filter(and_(models.Script.id == script_id, models.Script.user_id == userid)).delete()
    db.commit()
