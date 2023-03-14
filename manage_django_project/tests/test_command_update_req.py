from unittest.mock import patch

from django.core.management import call_command
from django.test import SimpleTestCase
from manageprojects.test_utils.subprocess import SubprocessCallMock

from manage_django_project.management.commands import shell, update_req
from manage_django_project.tests import PROJECT_ROOT
from manage_django_project.tests.cmd2_test_utils import BaseShellTestCase


class UpdateReqShellTestCase(BaseShellTestCase):
    def test_basic_update_req(self):
        with patch.object(shell, 'verbose_check_call') as call_mock:
            stdout, stderr = self.execute(command='update_req')
        self.assertEqual(stderr, '')
        self.assertIn('call command manage_django_project.update_req', stdout)
        call_mock.assert_called_once()


class UpdateReqTestCase(SimpleTestCase):
    maxDiff = None

    def test_basic_update_req(self):
        with SubprocessCallMock() as call_mock:
            call_command(update_req.Command())

        popenargs = call_mock.get_popenargs(rstrip_paths=(PROJECT_ROOT,))
        self.assertEqual(
            popenargs,
            [
                ['.../.venv/bin/pip', 'install', '-U', 'pip'],
                ['.../.venv/bin/pip', 'install', '-U', 'pip-tools'],
                [
                    '.../.venv/bin/pip-compile',
                    '--verbose',
                    '--allow-unsafe',
                    '--resolver=backtracking',
                    '--upgrade',
                    '--generate-hashes',
                    'pyproject.toml',
                    '--output-file',
                    'requirements.txt',
                ],
                [
                    '.../.venv/bin/pip-compile',
                    '--verbose',
                    '--allow-unsafe',
                    '--resolver=backtracking',
                    '--upgrade',
                    '--generate-hashes',
                    'pyproject.toml',
                    '--extra=dev',
                    '--output-file',
                    'requirements.dev.txt',
                ],
                ['.../.venv/bin/safety', 'check', '-r', 'requirements.dev.txt'],
                ['.../.venv/bin/pip-sync', 'requirements.dev.txt'],
            ],
        )
