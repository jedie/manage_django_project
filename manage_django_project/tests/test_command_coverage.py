from bx_py_utils.environ import OverrideEnviron
from django.test import SimpleTestCase

from manage_django_project.management.commands import coverage
from manage_django_project.tests.command_test_utils import EraseCoverageDataMixin, call_command_capture_subprocess


class CoverageTestCase(EraseCoverageDataMixin, SimpleTestCase):
    maxDiff = None

    def test_happy_path(self):
        with OverrideEnviron(
            TOX_ENV_NAME='foobar',  # env variable used to "detect" tox run
        ):
            popenargs = call_command_capture_subprocess(cmd_module=coverage)
        self.assertEqual(
            popenargs,
            [
                ['.../bin/coverage', 'run'],
            ],
        )

        with OverrideEnviron(
            TOX_ENV_NAME=None,  # Remove env variable that used to "detect" tox run
        ):
            popenargs = call_command_capture_subprocess(cmd_module=coverage)
        self.assertEqual(
            popenargs,
            [
                ['.../bin/coverage', 'run'],
                ['.../bin/coverage', 'combine', '--append'],
                ['.../bin/coverage', 'report'],
                ['.../bin/coverage', 'xml'],
                ['.../bin/coverage', 'json'],
                ['.../bin/coverage', 'erase'],
            ],
        )
