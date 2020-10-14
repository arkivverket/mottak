import logging
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_url():
    try:
        return "%s://%s:%s@%s/%s" % (
            os.environ["DB_DRIVER"],
            os.environ["DB_USER"],
            os.environ["DB_PASSWORD"],
            os.environ["DB_HOST"],
            os.environ["DB_NAME"],
        )
    except KeyError as exception:
        logging.error(f"Environment variable not set {exception}")
        sys.exit(1)


def get_session():
    engine = create_engine(get_url(), echo=True)
    session_class = sessionmaker()
    session_class.configure(bind=engine)
    return session_class()
