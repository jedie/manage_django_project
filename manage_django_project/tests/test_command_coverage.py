from django.test import SimpleTestCase

from manage_django_project.management.commands import coverage
from manage_django_project.tests.command_test_utils import call_command_capture_subprocess


class CoverageTestCase(SimpleTestCase):
    maxDiff = None

    def test_basic_update_req(self):
        popenargs = call_command_capture_subprocess(cmd_module=coverage)
        self.assertEqual(
            popenargs,
            [
                ['.../.venv/bin/coverage', 'run'],
                ['.../.venv/bin/coverage', 'combine', '--append'],
                ['.../.venv/bin/coverage', 'report'],
                ['.../.venv/bin/coverage', 'xml'],
                ['.../.venv/bin/coverage', 'json'],
            ],
        )
