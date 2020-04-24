import datetime
import time
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
)

logging.info("The example started")

SECRET = os.getenv("TEST_ENV_SECRET")

if SECRET is not None:
    # Secrets should not be logged!
    logging.info("The example found the env variable TEST_ENV_SECRET: {}".format(SECRET))
else:
    logging.warning("The example could not find the env variable TEST_ENV_SECRET")

while True:
    time.sleep(60)
    logging.info("The example ran for another minute")
