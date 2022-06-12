from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import and_

from dpapi.db import models
from dpapi.schema.dp_api import ScriptInDB, RunlogInDB


def create_script(db: Session, script: ScriptInDB):
    db_script = models.Script(name=script.name,
                              script_type=script.script_type,
                              content=script.content,
                              note=script.note,
                              created=script.created,
                              user_id=script.user_id)
    db.add(db_script)
    db.commit()
    db.refresh(db_script)
    return db_script


def get_scripts(db: Session, userid: str):
    return db.query(models.Script).filter_by(user_id=userid).order_by(models.Script.name).all()


def get_script(db: Session, userid: str, script_id: str):
    return db.query(models.Script).filter(and_(models.Script.user_id == userid, models.Script.id == script_id)).first()


def update_script(db: Session, script: ScriptInDB):
    db_script = db.query(models.Script) \
        .filter(and_(models.Script.id == script.id, models.Script.user_id == script.user_id)).first()
    if db_script:
        db_script.name = script.name
        db_script.script_type = script.script_type
        db_script.content = script.content
        db_script.note = script.note
        db_script.updated = script.updated
        db.commit()
        db.refresh(db_script)
    return db_script


def delete_script(db: Session, script_id: str, userid: str):
    db.query(models.Script).filter(and_(models.Script.id == script_id, models.Script.user_id == userid)).delete()
    db.commit()


def create_runlog(db: Session, runlog: RunlogInDB):
    db_runlog = models.RunLog(script_id=runlog.script_id,
                              requested=runlog.requested,
                              user_id=runlog.user_id)
    db.add(db_runlog)
    db.commit()
    db.refresh(db_runlog)
    return db_runlog


def get_runlogs(db: Session, userid: str, script_id: str):
    return db.query(models.RunLog).filter(and_(models.RunLog.user_id==userid, models.RunLog.script_id==script_id))\
        .order_by(models.RunLog.requested).all()


def update_runlog(db: Session, runlog: RunlogInDB):
    db_runlog = db.query(models.RunLog) \
        .filter(and_(models.RunLog.id == runlog.id, models.RunLog.user_id == runlog.user_id)).first()
    if db_runlog:
        db_runlog.started = runlog.started
        db_runlog.finished = runlog.finished
        db_runlog.status = runlog.status
        db.commit()
        db.refresh(db_runlog)
    return db_runlog


def delete_runlog(db: Session, runlog_id: str, userid: str):
    db.query(models.Script).filter(and_(models.RunLog.id == runlog_id, models.RunLog.user_id == userid)).delete()
    db.commit()
