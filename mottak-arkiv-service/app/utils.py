import pytz

from datetime import datetime
from pathlib import Path


def get_project_root() -> Path:
    """
    This method is used when building absolute Paths.
    Relative Paths isn't functioning when using pytest from root.
    :return:
    """
    return Path(__file__).parent.parent


def convert_string_to_datetime(datetime_string: str):
    iso_8601 = '%Y-%m-%dT%H:%M:%S%z'
    return datetime.strptime(datetime_string, iso_8601).astimezone(pytz.timezone("Europe/Oslo"))
