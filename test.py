# Import Pytest
import pytest
from database import Base, get_db_conn
from exceptions import WTPDuplicateException, WTPNotFoundException
from main import open_db_connections, close_db_connections
from models import TimeSheetDB
from service import TimeSheetService
from utils import get_current_time
from sqlalchemy.orm import Session


@pytest.fixture(scope="module")
def test_session():
    open_db_connections()
    engine = get_db_conn()
    Base.metadata.create_all(bind=engine)
    db = Session(bind=engine)
    yield db

    # Drop all tables
    Base.metadata.drop_all(engine)
    close_db_connections()


class TestTimeSheetService:
    #  autouse makes the function run before each test method. This fixture function does setup and teardown.
    @pytest.fixture(autouse=True)
    @pytest.mark.usefixtures("test_session")
    def setup_and_teardown(self, test_session):
        self.service = TimeSheetService(test_session)

        stored_timesheet = TimeSheetDB(task_id=1, user_id=3)
        self.stored_timesheet = stored_timesheet
        self.stored_timesheet.date_clocked_in = get_current_time()

    # Each test needs to re-create TimeSheetService in order for the mock of get_timesheet not to leak into other tests.
    def test_clock_in_new_timesheet(self):
        try:
            self.service.clock_in(
                self.stored_timesheet.user_id, self.stored_timesheet.task_id
            )
        except Exception as e:
            assert False, str(e)
        else:
            assert True

    def test_clock_in_raises_exception_for_existing_timesheet(self):
        with pytest.raises(WTPDuplicateException):
            self.service.clock_in(
                self.stored_timesheet.user_id, self.stored_timesheet.task_id
            )

    def test_clock_out_existing_timesheet(self):
        try:
            self.service.clock_out(
                self.stored_timesheet.user_id, self.stored_timesheet.task_id
            )
        except Exception as e:
            assert False, str(e)

    def test_clock_out_no_timesheet(self):
        with pytest.raises(WTPNotFoundException):
            self.service.clock_out(3, 20)
