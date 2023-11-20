from sqlalchemy.orm import Session
from exceptions import WTPDuplicateException, WTPNotFoundException
from models import TimeSheetDB
from schemas import TimeSheet, TimeSheetOut
from utils import get_current_time


class TimeSheetService:
    db: Session

    def __init__(self, db: Session) -> None:
        self.db = db

    def clock_in(self, user_id: int, task_id: int) -> TimeSheet:
        """Clocks the user in. The function will create a new timesheet for this user with the corresponding task."""

        if self.get_timesheet(task_id=task_id, user_id=user_id) is not None:
            raise WTPDuplicateException("There is a timesheet for this task already.")

        # * Create a new time sheet for this user
        timesheet = TimeSheetDB(
            task_id=task_id, user_id=user_id, date_clocked_in=get_current_time()
        )

        # * persist this into the database
        self.db.add(timesheet)
        self.db.commit()
        self.db.refresh(timesheet)

        return timesheet

    def clock_out(self, user_id: int, task_id: int) -> TimeSheet:
        timesheet: TimeSheetDB = self.get_timesheet(user_id=user_id, task_id=task_id)
        print(timesheet)
        if timesheet is None:
            raise WTPNotFoundException(
                "There is no timesheet for this task, kindly clock in."
            )
        timesheet.date_clocked_out = get_current_time()
        # * persist this into the database
        self.db.add(timesheet)
        self.db.commit()
        self.db.refresh(timesheet)

        return TimeSheetOut.model_validate(timesheet)

    def get_timesheet(self, task_id: int, user_id: int) -> TimeSheet:
        return (
            self.db.query(TimeSheetDB)
            .filter(TimeSheetDB.task_id == task_id, TimeSheetDB.user_id == user_id)
            .first()
        )
