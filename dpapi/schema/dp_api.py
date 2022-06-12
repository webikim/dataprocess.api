from datetime import datetime
from typing import Union

from pydantic import BaseModel


class ScriptBase(BaseModel):
    id: Union[str, None]
    name: str


class Script(ScriptBase):
    script_type: str
    content: str
    note: str


class ScriptCreate(Script):
    pass


class ScriptInDB(Script):
    created: Union[datetime, None]
    updated: Union[datetime, None]
    user_id: str


class RunlogBase(BaseModel):
    id: Union[str, None]


class Runlog(RunlogBase):
    script_id: str
    requested: Union[datetime, None]
    started: Union[datetime, None]
    finished: Union[datetime, None]
    status: Union[str, None]


class RunlogInDB(Runlog):
    user_id: str
