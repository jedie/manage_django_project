import shutil
from pathlib import Path

import django
from bx_py_utils.path import assert_is_file
from cli_base.cli_tools.subprocess_utils import verbose_check_output

from manage_django_project.tests import PROJECT_ROOT


def get_django_main_version() -> str:
    """
    Get the main Django version as a string, e.g. '5.2'.
    """
    return '.'.join(str(x) for x in django.VERSION[:2])


class CallManagePy:
    manage_py_filename = 'manage.py'

    def __init__(self, project_root: Path = PROJECT_ROOT):
        self.project_root = project_root
        assert_is_file(self.project_root / self.manage_py_filename)

        self.system_python_bin = shutil.which('python3')
        assert 'python' in self.system_python_bin, f'{self.system_python_bin=}'

    def verbose_check_output(self, *args):
        output = verbose_check_output(
            self.system_python_bin, self.manage_py_filename, *args, verbose=False, cwd=PROJECT_ROOT
        )
        return output
