import os
import sys

# SECRET = os.getenv("TEST_SECRET")
# if SECRET is not None:
#     print("The secret is: " + SECRET) # Secrets should not be logged!
# else:
#     print("Something is wrong, could not find the env variable TEST_SECRET", file=sys.stderr)

print("The example ran")
sys.exit(os.EX_OK)

