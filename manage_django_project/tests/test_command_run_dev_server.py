from unittest.mock import patch

from bx_py_utils.test_utils.snapshot import assert_text_snapshot
from cmd2.ansi import strip_style
from django.test import SimpleTestCase
from django_tools.management.commands import run_testserver
from django_tools.unittest_utils.call_management_commands import captured_call_command

from manage_django_project.management.commands import run_dev_server, shell
from manage_django_project.tests.cmd2_test_utils import BaseShellTestCase


class RunDevServerShellTestCase(BaseShellTestCase):
    def test_basic_run_dev_server(self):
        with patch.object(shell, 'verbose_check_call') as call_mock:
            stdout, stderr = self.execute(command='run_dev_server')
        self.assertEqual(stderr, '')
        self.assertIn('call command manage_django_project.run_dev_server', stdout)
        call_mock.assert_called_once()


class RunDevServerTestCase(SimpleTestCase):
    maxDiff = None

    def test_basic_run_dev_server(self):
        with patch.object(run_testserver, 'call_command') as call_command_mock:
            output, stderr = captured_call_command(
                run_dev_server,
            )

        self.assertEqual(stderr, '')

        output = strip_style(output)

        self.assertIn('makemigrations', output)
        self.assertIn('migrate', output)
        self.assertIn('runserver', output)

        call_command_mock.assert_called()

        assert_text_snapshot(got=output)
