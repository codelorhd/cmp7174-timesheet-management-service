

from fastapi import APIRouter, Security
from dependencies import initiate_timesheet_service
from schemas import ClockIn
from service import TimeSheetService

from utils import http_responses


router = APIRouter(tags=["Timesheet"], prefix="/time-sheet", responses=http_responses)


@router.post(
    "/clock-in",
    # response_model=str,
)
def clock_in(
    data: ClockIn,
    timesheet_service: TimeSheetService = Security(
            initiate_timesheet_service
    ),
):
    """ Allows the worker to clock in. """
    timesheet_service.clock_in(user_id=data.user_id, task_id=data.task_id)