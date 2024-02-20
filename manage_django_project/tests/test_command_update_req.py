import inspect
import re
from unittest.mock import patch

from bx_py_utils.test_utils.redirect import RedirectOut
from bx_py_utils.test_utils.snapshot import assert_snapshot
from django.test import SimpleTestCase

from manage_django_project.management.commands import shell, update_req
from manage_django_project.tests.cmd2_test_utils import BaseShellTestCase
from manage_django_project.tests.command_test_utils import call_command_capture_subprocess


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
        with RedirectOut() as buffer:
            popenargs = call_command_capture_subprocess(cmd_module=update_req)

        self.assertEqual(buffer.stderr, '')

        blocks = re.split(r'-{10,}', buffer.stdout)
        last_block = blocks[-1]
        self.assertEqual(
            last_block.strip(),
            inspect.cleandoc('''
                Generate requirement files:
                 * requirements.txt
                 * requirements.dev.txt
                 * requirements.django32.txt
                 * requirements.django42.txt
                 * requirements.django50.txt

                Install requirement from: requirements.django50.txt
                ''').strip(),
        )

        # Check samples:
        self.assertEqual(popenargs[0], ['.../bin/pip', 'install', '-U', 'pip'])
        self.assertEqual(popenargs[-1], ['.../bin/pip-sync', 'requirements.django50.txt'])
        assert_snapshot(got=popenargs)
