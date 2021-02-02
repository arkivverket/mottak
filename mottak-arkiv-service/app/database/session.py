import logging
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


def _get_url():
    try:
        return os.environ["DBSTRING"]
    except KeyError as exception:
        logger.error(f"Environment variable not set {exception}")
        sys.exit(1)


def get_session():
    engine = create_engine(_get_url())
    session_class = sessionmaker()
    session_class.configure(bind=engine)
    return session_class()
