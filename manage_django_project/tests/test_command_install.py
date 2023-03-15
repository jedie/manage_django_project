from unittest.mock import patch

from django.test import SimpleTestCase

from manage_django_project.management.commands import install, shell
from manage_django_project.tests.cmd2_test_utils import BaseShellTestCase
from manage_django_project.tests.command_test_utils import call_command_capture_subprocess


class InstallShellTestCase(BaseShellTestCase):
    def test_basic_install(self):
        with patch.object(shell, 'verbose_check_call') as call_mock:
            stdout, stderr = self.execute(command='install')
        self.assertEqual(stderr, '')
        self.assertIn('call command manage_django_project.install', stdout)
        call_mock.assert_called_once()


class InstallTestCase(SimpleTestCase):
    maxDiff = None

    def test_basic_install(self):
        popenargs = call_command_capture_subprocess(cmd_module=install)
        self.assertEqual(
            popenargs,
            [
                ['.../bin/pip', 'install', '--no-deps', '-e', '.'],
            ],
        )
