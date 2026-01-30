from unittest.mock import patch

from bx_py_utils.test_utils.redirect import RedirectOut
from cli_base.cli_tools.test_utils.temp_utils import FakeNamedTemporaryFile
from django.core.management import call_command
from django.test import SimpleTestCase
from manageprojects.test_utils.subprocess import SimpleRunReturnCallback, SubprocessCallMock

from manage_django_project.management.commands import shell, update_req
from manage_django_project.tests.cmd2_test_utils import BaseShellTestCase
from manage_django_project.tests.command_test_utils import get_rstrip_paths


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
        with (
            RedirectOut() as buffer,
            SubprocessCallMock(
                return_callback=SimpleRunReturnCallback(stdout=b'mocked output'),  # type: ignore
            ) as call_mock,
            patch('tempfile.NamedTemporaryFile', FakeNamedTemporaryFile),
        ):
            call_command(update_req.Command())

        popenargs = call_mock.get_popenargs(rstrip_paths=get_rstrip_paths())

        self.assertEqual(buffer.stderr, '')
        self.assertIn('Update project requirements via uv', buffer.stdout)

        # Check samples:
        self.assertEqual(popenargs[0], ['.../bin/pip', 'install', '-U', 'pip'])
        self.assertEqual(popenargs[-1], ['.../bin/pre-commit', 'autoupdate'])
