from unittest import TestCase

from manage_django_project import __version__
from manage_django_project.test_utilities import CallManagePy


class ManageTestCase(TestCase):
    maxDiff = None

    def test_manage_py_call(self):
        manage_py = CallManagePy()

        output = manage_py.verbose_check_output('--version')
        self.assertIn(__version__, output)  # Check Django version

        output = manage_py.verbose_check_output('--help')
        self.assertIn('.venv/bin/manage_django_project_example --help', output)
        self.assertIn('manage_django_project_example help <subcommand>', output)
        self.assertIn('Available subcommands:', output)
        self.assertIn('[django]', output)
        self.assertIn('[manage_django_project]', output)
        self.assertIn('project_info', output)

        output = manage_py.verbose_check_output('project_info')
        self.assertIn('manage_config = ProjectInfo(', output)
        self.assertIn("local_settings='manage_django_project_example.settings.local',", output)
        self.assertIn("test_settings='manage_django_project_example.settings.tests',", output)

        output = manage_py.verbose_check_output('check')
        self.assertIn('System check identified no issues (0 silenced).', output)

        output = manage_py.verbose_check_output('makemigrations')
        self.assertIn("No changes detected", output)
