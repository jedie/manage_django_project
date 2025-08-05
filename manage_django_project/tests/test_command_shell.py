from bx_py_utils.test_utils.snapshot import assert_text_snapshot

from manage_django_project.test_utilities import get_django_main_version
from manage_django_project.tests.cmd2_test_utils import BaseShellTestCase


class ManageDjangoShellTestCase(BaseShellTestCase):
    def test_help(self):
        stdout, stderr = self.execute(command='help')
        self.assertEqual(stderr, '')
        self.assertIn('Documented commands', stdout)
        self.assertIn('django.core', stdout)
        self.assertIn('makemessages', stdout)
        self.assertIn('makemigrations', stdout)
        self.assertIn('manage_django_project', stdout)
        self.assertIn('run_dev_server', stdout)

        assert_text_snapshot(
            got=stdout,
            snapshot_name=f'test_command_shell_help_django{get_django_main_version()}',
        )
