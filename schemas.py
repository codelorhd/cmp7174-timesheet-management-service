import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class DB_BaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ClockIn(BaseModel):
    task_id: int
    user_id: int


class ClockOut(BaseModel):
    task_id: int
    user_id: int


class TimeSheet(BaseModel):
    task_id: int
    user_id: int


class TimeSheetOut(DB_BaseModel):
    task_id: int
    user_id: int
    date_clocked_in: datetime.datetime
    date_clocked_out: Optional[datetime.datetime]


class ManyTimeSheets(BaseModel):
    total: int
    sheets: List[TimeSheet]
