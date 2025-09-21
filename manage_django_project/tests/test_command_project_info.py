from unittest.mock import patch

from bx_py_utils.test_utils.snapshot import assert_text_snapshot
from cli_base.cli_tools.test_utils.rich_test_utils import NoColorEnvRich
from django.test import SimpleTestCase
from django_tools.unittest_utils.call_management_commands import captured_call_command

from manage_django_project import __version__
from manage_django_project.management.commands import project_info, shell
from manage_django_project.tests import PROJECT_ROOT
from manage_django_project.tests.cmd2_test_utils import BaseShellTestCase


class ProjectInfoShellTestCase(BaseShellTestCase):
    def test_basic_project_info(self):
        with patch.object(shell, 'verbose_check_call') as call_mock:
            stdout, stderr = self.execute(command='project_info')
        self.assertEqual(stderr, '')
        self.assertIn('call command manage_django_project.project_info', stdout)
        call_mock.assert_called_once()


class InstallTestCase(SimpleTestCase):
    maxDiff = None

    def test_project_info(self):
        with NoColorEnvRich(width=120):
            output, stderr = captured_call_command(project_info)
        self.assertEqual(stderr, '')
        self.assertIn('manage_config = ProjectInfo(', output)
        self.assertIn("distribution_name='manage_django_project',", output)

        path_str = str(PROJECT_ROOT.parent)
        self.assertIn(path_str, output)
        stdout_output = output.replace(path_str, '...')

        self.assertIn(__version__, stdout_output)
        stdout_output = stdout_output.replace(__version__, '<mocked>')

        assert_text_snapshot(got=stdout_output)
