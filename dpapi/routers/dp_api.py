import datetime

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from dpapi.db import get_db
from dpapi.db import dp_crud
from dpapi.routers.login import get_user_id
from dpapi.schema.dp_api import ScriptCreate, ScriptInDB, ScriptBase, RunlogInDB, Runlog

router = APIRouter(prefix='/dpapi')

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")


@router.post('/script')
def script_create(param: ScriptCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_schema)):
    userid = get_user_id(token)
    db_script = ScriptInDB(name=param.name, script_type=param.script_type, content=param.content, note=param.note, user_id=userid)
    if param.id is not None and int(param.id) >= 0:
        db_script.id = param.id
        db_script.updated = datetime.datetime.utcnow()
        return dp_crud.update_script(db, db_script)
    else:
        db_script.created = datetime.datetime.utcnow()
        return dp_crud.create_script(db, db_script)


@router.get('/script')
def script_get(script_id: str, token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    userid = get_user_id(token)
    return dp_crud.get_script(db, userid, script_id)


@router.delete('/script')
def script_delete(script_id: str, token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    userid = get_user_id(token)
    script = dp_crud.delete_script(db, script_id, userid)
    return 'OK' if script is None else 'NOK'


@router.get('/script/list')
def script_list(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    userid = get_user_id(token)
    return [ScriptBase(id=each.id, name=each.name) for each in dp_crud.get_scripts(db, userid)]


@router.post('/run')
def run_create(param: Runlog, db: Session = Depends(get_db), token: str = Depends(oauth2_schema)):
    userid = get_user_id(token)
    db_runlog = RunlogInDB(script_id=param.script_id, user_id=userid)
    if param.id is not None and int(param.id) >= 0:
        db_runlog.started = param.started
        db_runlog.finished = param.finished
        db_runlog.status = param.status
    else:
        db_runlog.requested = datetime.datetime.utcnow()
    return dp_crud.create_runlog(db, db_runlog)


@router.delete('/run')
def run_delete():
    pass


@router.get('/run/list')
def run_list(script_id: str, db: Session = Depends(get_db), token: str = Depends(oauth2_schema)):
    userid = get_user_id(token)
    return dp_crud.get_runlogs(db, userid, script_id)