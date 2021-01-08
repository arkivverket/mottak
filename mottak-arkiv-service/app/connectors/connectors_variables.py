import os


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


def get_tusd_url() -> str:
    """
    Gets env variable for public tusd url
    :return: tusd public url
    """
    # TODO handle KeyError
    return os.environ['TUSD_URL']


def get_sas_url() -> str:
    """
    Gets env variable for SAS generator url
    :retrurn sas url
    """
    # TODO handle KeyError
    return os.environ['SAS_URL']
