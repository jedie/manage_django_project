from unittest.mock import patch

from django.test import SimpleTestCase

from manage_django_project.management.commands import pip_audit, shell
from manage_django_project.tests.cmd2_test_utils import BaseShellTestCase
from manage_django_project.tests.command_test_utils import call_command_capture_subprocess


class FakeNamedTemporaryFile:
    def __init__(self, prefix: str = 'prefix', suffix: str = 'suffix'):
        self.name = f'/tmp/{prefix}<rnd>{suffix}'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


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
        with patch('tempfile.NamedTemporaryFile', FakeNamedTemporaryFile):
            popenargs = call_command_capture_subprocess(cmd_module=pip_audit)
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
                    '-o',
                    '/tmp/requirements<rnd>.txt',
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
