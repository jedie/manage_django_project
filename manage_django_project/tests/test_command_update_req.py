from unittest.mock import patch

from manage_django_project.management.commands import shell
from manage_django_project.tests.cmd2_test_utils import BaseShellTestCase


class ManageDjangoShellTestCase(BaseShellTestCase):
    def test_basic_update_req(self):
        with patch.object(shell, 'verbose_check_call') as call_mock:
            stdout, stderr = self.execute(command='update_req')
        self.assertEqual(stderr, '')
        self.assertIn('call command manage_django_project.update_req', stdout)
        call_mock.assert_called_once()
