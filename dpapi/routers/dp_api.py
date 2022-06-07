import datetime

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from dpapi.db import get_db
from dpapi.db import dp_crud
from dpapi.routers.login import get_user_id
from dpapi.schema.dp_api import ScriptCreate, ScriptInDB

router = APIRouter(prefix='/dpapi')

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")


@router.post('/script')
def script_create(param: ScriptCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_schema)):
    userid = get_user_id(token)
    db_script = ScriptInDB(name=param.name, content=param.content, note=param.note, user_id=userid)
    if param.script_id is not None and int(param.script_id) >= 0:
        db_script.script_id = param.script_id
        db_script.updated = datetime.datetime.utcnow()
        return dp_crud.update_script(db, db_script)
    else:
        db_script.created = datetime.datetime.utcnow()
        return dp_crud.create_script(db, db_script)


@router.get('/script')
def script_get(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    userid = get_user_id(token)
    return dp_crud.get_script(db, userid)


@router.delete('/script')
def script_delete(script_id: str, token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    userid = get_user_id(token)
    script = dp_crud.delete_script(db, script_id, userid)
    return 'OK' if script is None else 'NOK'
