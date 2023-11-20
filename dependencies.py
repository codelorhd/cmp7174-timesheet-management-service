from sqlalchemy.orm import Session
from fastapi import Depends

from database import get_db_sess
from service import TimeSheetService


def initiate_timesheet_service( db: Session = Depends(get_db_sess) ):
    return TimeSheetService(db =  db) 