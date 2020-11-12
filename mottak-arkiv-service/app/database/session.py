import logging
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def _get_url():
    try:
        return os.environ["DBSTRING"]
    except KeyError as exception:
        logging.error(f"Environment variable not set {exception}")
        sys.exit(1)


def get_session():
    engine = create_engine(_get_url(), echo=True)
    session_class = sessionmaker()
    session_class.configure(bind=engine)
    return session_class()
