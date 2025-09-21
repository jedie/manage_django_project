from cli_base.cli_tools.test_utils.rich_test_utils import NoColorEnvRich
from django.test import SimpleTestCase

from manage_django_project.test_utilities import CallManagePy


class TestCase(SimpleTestCase):
    maxDiff = None

    def test_happy_path(self):
        manage_py = CallManagePy()
        with NoColorEnvRich(width=80):
            output = manage_py.verbose_check_output('playwright', '--help')

        self.assertIn('manage_django_project_example playwright --help\n', output)
        self.assertIn('Usage: playwright [options] [command]\n', output)
        self.assertIn('Call playwright CLI', output)
        self.assertIn('install [options] [browser...]', output)
