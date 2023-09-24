import shutil
from unittest import TestCase

from bx_py_utils.path import assert_is_file
from cli_base.cli_tools.subprocess_utils import verbose_check_output

from manage_django_project import __version__
from manage_django_project.tests import PROJECT_ROOT


def call_manage_py(*args) -> str:
    assert_is_file(PROJECT_ROOT / 'manage.py')

    system_python_bin = shutil.which('python3')
    assert 'python' in system_python_bin, f'{system_python_bin=}'

    output = verbose_check_output(system_python_bin, 'manage.py', *args, verbose=False, cwd=PROJECT_ROOT)
    return output


class ManageTestCase(TestCase):
    def test_manage_py_call(self):
        output = call_manage_py('--version')
        self.assertIn(__version__, output)  # Check Django version will not work with tox!

        output = call_manage_py('--help')
        self.assertIn('.venv/bin/manage_django_project_example --help', output)
        self.assertIn('manage_django_project_example help <subcommand>', output)
        self.assertIn('Available subcommands:', output)
        self.assertIn('[django]', output)
        self.assertIn('[manage_django_project]', output)
        self.assertIn('project_info', output)
