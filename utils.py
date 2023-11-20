import datetime
from typing import Dict, Union


http_responses: Dict[Union[str, int], Dict[str, str]] = {
    404: {"description": "Not found"},
    413: {"description": "File too large"},
    403: {"description": "Not Authorized"},
    409: {"description": "Duplicate Resource"},
    500: {"description": "Internal Server Error"},
    503: {"description": "Service Unavailable"},
}


def get_current_time():
    return datetime.datetime.now(datetime.timezone.utc)
