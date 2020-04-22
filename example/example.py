import os
import sys

SECRET = os.getenv("EXAMPLE_SECRET")

if SECRET is not None:
    print("The secret is: " + SECRET) # Secrets should not be logged!
else:
    print("Something is wrong, could not find the env variable EXAMPLE_SECRET", file=sys.stderr)
