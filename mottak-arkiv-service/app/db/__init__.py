from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def Session():
    engine = create_engine(getenv('DSN'), echo=True)
    session_class = sessionmaker()
    session_class.configure(bind=engine)
    return session_class()

