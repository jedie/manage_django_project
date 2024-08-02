from unittest.mock import patch

from django.test import SimpleTestCase

from manage_django_project.management.commands import pip_audit, shell
from manage_django_project.tests.cmd2_test_utils import BaseShellTestCase
from manage_django_project.tests.command_test_utils import call_command_capture_subprocess


class PipAuditShellTestCase(BaseShellTestCase):
    def test_basic_safety(self):
        with patch.object(shell, 'verbose_check_call') as call_mock:
            stdout, stderr = self.execute(command='pip_audit')
        self.assertEqual(stderr, '')
        self.assertIn('call command manage_django_project.pip_audit', stdout)
        call_mock.assert_called_once()


class PipAuditTestCase(SimpleTestCase):
    maxDiff = None

    def test_basic_safety(self):
        popenargs = call_command_capture_subprocess(cmd_module=pip_audit)
        self.assertEqual(
            popenargs,
            [
                ['.../bin/pip-audit', '-v', '--strict', '--require-hashes', '-r', 'requirements.dev.txt'],
            ],
        )
