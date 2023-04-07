import shutil
from unittest import TestCase

from bx_py_utils.path import assert_is_file
from manageprojects.utilities.subprocess_utils import verbose_check_output

from manage_django_project import __version__
from manage_django_project.tests import PROJECT_ROOT


class ManageTestCase(TestCase):
    def test_manage_py_call(self):
        assert_is_file(PROJECT_ROOT / 'manage.py')

        system_python_bin = shutil.which('python3')
        self.assertIn('python', system_python_bin)

        output = verbose_check_output(system_python_bin, 'manage.py', '--version', verbose=False, cwd=PROJECT_ROOT)
        self.assertIn('.venv/bin/manage_django_project_example --version', output)
        self.assertIn(__version__, output)  # Check Django version will not work with tox!

        output = verbose_check_output(system_python_bin, 'manage.py', '--help', verbose=False, cwd=PROJECT_ROOT)
        self.assertIn('.venv/bin/manage_django_project_example --help', output)
        self.assertIn('manage_django_project_example help <subcommand>', output)
        self.assertIn('Available subcommands:', output)
        self.assertIn('[django]', output)
        self.assertIn('[manage_django_project]', output)
        self.assertIn('project_info', output)
