from django.test import SimpleTestCase

from manage_django_project.tests.command_test_utils import ForceRichTerminalWidth
from manage_django_project.tests.test_manage import call_manage_py


class TestCase(SimpleTestCase):
    maxDiff = None

    def test_happy_path(self):
        with ForceRichTerminalWidth(width=80):
            output = call_manage_py('playwright', '--help')

        self.assertIn('manage_django_project_example playwright --help\n', output)
        self.assertIn('Usage: playwright [options] [command]\n', output)
        self.assertIn('Playwright Test', output)
        self.assertIn('install [options] [browser...]', output)
