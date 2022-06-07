from datetime import datetime
from typing import Union

from pydantic import BaseModel


class ScriptBase(BaseModel):
    script_id: Union[str, None]
    name: str
    content: str
    note: str


class ScriptCreate(ScriptBase):
    pass


class ScriptInDB(ScriptBase):
    created: Union[datetime, None]
    updated: Union[datetime, None]
    user_id: str
