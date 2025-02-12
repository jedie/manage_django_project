from unittest.mock import patch

from bx_py_utils.environ import OverrideEnviron
from django.test import SimpleTestCase
from manageprojects.test_utils.subprocess import SubprocessCallMock

from manage_django_project.management.commands import nox, shell
from manage_django_project.tests.cmd2_test_utils import BaseShellTestCase
from manage_django_project.tests.command_test_utils import EraseCoverageDataMixin, get_rstrip_paths


class NoxShellTestCase(BaseShellTestCase):
    def test_basic_nox(self):
        with patch.object(shell, 'verbose_check_call') as call_mock:
            stdout, stderr = self.execute(command='nox')
        self.assertEqual(stderr, '')
        self.assertIn('call command manage_django_project.nox', stdout)
        call_mock.assert_called_once()


class NoxTestCase(EraseCoverageDataMixin, SimpleTestCase):
    maxDiff = None

    def test_basic_nox(self):
        command = nox.Command()
        with (
            SubprocessCallMock() as call_mock,
            OverrideEnviron(
                nox_ENV_NAME='foobar',  # env variable used to "detect" nox run
            ),
        ):
            try:
                command.run_from_argv(argv=['--foo', '--bar'])
            except SystemExit as err:
                self.assertEqual(err.code, 0)

        popenargs = call_mock.get_popenargs(rstrip_paths=get_rstrip_paths())
        self.assertEqual(
            popenargs,
            [
                ['.../bin/nox'],
                ['.../bin/coverage', 'combine', '--append'],
                ['.../bin/coverage', 'report'],
                ['.../bin/coverage', 'xml'],
                ['.../bin/coverage', 'json'],
                ['.../bin/coverage', 'erase'],
            ],
        )
