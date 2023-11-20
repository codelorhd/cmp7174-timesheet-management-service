import datetime
from sqlalchemy import Column, DateTime, Integer

from database import Base


class TimeSheetDB(Base):
    __tablename__ = "timesheet"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=False, index=False)
    task_id = Column(Integer, unique=False, index=False)
    date_created = Column(
        DateTime, default=datetime.datetime.now(datetime.timezone.utc)
    )
    date_clocked_in = Column(
        DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=True
    )
    date_clocked_out = Column(DateTime, nullable=True)
