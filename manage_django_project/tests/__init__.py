import unittest.util
from pathlib import Path

import manage_django_project


PROJECT_ROOT = Path(manage_django_project.__file__).parent.parent


# Hacky way to expand the failed test output:
unittest.util._MAX_LENGTH = 200
