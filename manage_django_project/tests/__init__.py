import unittest.util
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent.parent


# Hacky way to expand the failed test output:
unittest.util._MAX_LENGTH = 200
