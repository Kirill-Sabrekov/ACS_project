from pydantic import BaseModel
from typing import Optional, List
import datetime
import uuid

class SensorHistorySchema(BaseModel):
    actualtime: Optional[datetime.datetime]
    time: Optional[datetime.datetime]
    valint: Optional[int]
    valuint: Optional[int]
    valdouble: Optional[float]
    valbool: Optional[bool]
    valstring: Optional[str]
    quality: Optional[int]
    recordtype: Optional[str]
    appid: Optional[uuid.UUID]

    class Config:
        orm_mode = True

class NodeSchema(BaseModel):
    nodeid: int
    tagname: str
    history: List[SensorHistorySchema]

    class Config:
        orm_mode = True

class NodeShortSchema(BaseModel):
    nodeid: int
    tagname: str

    class Config:
        orm_mode = True 