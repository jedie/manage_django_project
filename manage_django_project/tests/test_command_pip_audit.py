from unittest.mock import patch

from bx_py_utils.test_utils.redirect import RedirectOut
from cli_base.cli_tools.test_utils.temp_utils import FakeNamedTemporaryFile
from django.core.management import call_command
from django.test import SimpleTestCase
from manageprojects.test_utils.subprocess import SimpleRunReturnCallback, SubprocessCallMock

from manage_django_project.management.commands import pip_audit, shell
from manage_django_project.tests.cmd2_test_utils import BaseShellTestCase
from manage_django_project.tests.command_test_utils import get_rstrip_paths


class PipAuditShellTestCase(BaseShellTestCase):
    def test_pip_audit(self):
        with patch.object(shell, 'verbose_check_call') as call_mock:
            stdout, stderr = self.execute(command='pip_audit')
        self.assertEqual(stderr, '')
        self.assertIn('call command manage_django_project.pip_audit', stdout)
        call_mock.assert_called_once()


class PipAuditTestCase(SimpleTestCase):
    maxDiff = None

    def test_pip_audit(self):
        with (
            RedirectOut() as buffer,
            SubprocessCallMock(
                return_callback=SimpleRunReturnCallback(stdout=b'mocked output'),  # type: ignore
            ) as call_mock,
            patch('tempfile.NamedTemporaryFile', FakeNamedTemporaryFile),
        ):
            call_command(pip_audit.Command())

        self.assertEqual(buffer.stderr, '')
        self.assertIn('Run `pip-audit` with configuration from `pyproject', buffer.stdout)

        popenargs = call_mock.get_popenargs(rstrip_paths=get_rstrip_paths())
        self.assertEqual(
            popenargs,
            [
                [
                    '.../bin/uv',
                    'export',
                    '--no-header',
                    '--frozen',
                    '--no-editable',
                    '--no-emit-project',
                ],
                [
                    '.../bin/pip-audit',
                    '--strict',
                    '--require-hashes',
                    '--disable-pip',
                    '-v',
                    '-r',
                    '/tmp/requirements<rnd>.txt',
                ],
            ],
        )
