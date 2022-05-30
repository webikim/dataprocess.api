from pydantic import BaseModel


class AnnoMeta(BaseModel):
    path: str
    name: str


class Anno(AnnoMeta):
    data: dict
