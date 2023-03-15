from unittest.mock import patch

from django.test import SimpleTestCase
from manageprojects.test_utils.subprocess import SubprocessCallMock

from manage_django_project.management.commands import shell, tox
from manage_django_project.tests import PROJECT_ROOT
from manage_django_project.tests.cmd2_test_utils import BaseShellTestCase


class ToxShellTestCase(BaseShellTestCase):
    def test_basic_tox(self):
        with patch.object(shell, 'verbose_check_call') as call_mock:
            stdout, stderr = self.execute(command='tox')
        self.assertEqual(stderr, '')
        self.assertIn('call command manage_django_project.tox', stdout)
        call_mock.assert_called_once()


class ToxTestCase(SimpleTestCase):
    maxDiff = None

    def test_basic_tox(self):
        command = tox.Command()
        with SubprocessCallMock() as call_mock:
            try:
                command.run_from_argv(argv=['--foo', '--bar'])
            except SystemExit as err:
                self.assertEqual(err.code, 0)

        popenargs = call_mock.get_popenargs(rstrip_paths=(PROJECT_ROOT,))
        self.assertEqual(
            popenargs,
            [
                ['.../.venv/bin/python', '-m', 'tox'],
                ['.../.venv/bin/coverage', 'combine', '--append'],
                ['.../.venv/bin/coverage', 'report'],
                ['.../.venv/bin/coverage', 'xml'],
                ['.../.venv/bin/coverage', 'json'],
            ],
        )
