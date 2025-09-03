from unittest.mock import patch

from django.test import SimpleTestCase

from manage_django_project.management.commands import code_style, shell
from manage_django_project.tests.cmd2_test_utils import BaseShellTestCase
from manage_django_project.tests.command_test_utils import call_command_capture_subprocess


class CodeStyleShellTestCase(BaseShellTestCase):
    def test_basic_code_style(self):
        with patch.object(shell, 'verbose_check_call') as call_mock:
            stdout, stderr = self.execute(command='code_style')
        self.assertEqual(stderr, '')
        self.assertIn('call command manage_django_project.code_style', stdout)
        call_mock.assert_called_once()


class CodeStyleTestCase(SimpleTestCase):
    maxDiff = None

    def test_basic_code_style(self):
        popenargs = call_command_capture_subprocess(cmd_module=code_style)
        self.assertEqual(popenargs, [['.../bin/ruff', 'check', '--fix']])
