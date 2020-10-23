import os
from app.database.session import get_session


async def get_db_session():
    try:
        db = get_session()
        yield db
    finally:
        db.close()


def get_mailgun_domain() -> str:
    """
    Gets env variable for mailgun domain
    :return: mailgun domain
    """
    # TODO handle KeyError
    return os.environ["MAILGUN_DOMAIN"]


def get_mailgun_secret() -> str:
    """
    Gets env variable for mailgun api secret
    :return: mailgun api secret
    """
    # TODO handle KeyError
    return os.environ['MAILGUN_SECRET']
