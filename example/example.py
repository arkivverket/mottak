import datetime
import time
import os
import sys

print("The example started")

SECRET = os.getenv("TEST_SECRET")

if SECRET is not None:
    print("The example found the env variable TEST_SECRET: " + SECRET) # Secrets should not be logged!
else:
    print("The example could not find the env variable TEST_SECRET", file=sys.stderr)

while True:
    time.sleep(60)
    print("The example ran for another minute", datetime.datetime.now().time())

