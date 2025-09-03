from types import ModuleType

from django.core.management import call_command
from django.test import SimpleTestCase
from manageprojects.test_utils.project_setup import check_editor_config, get_py_max_line_length
from packaging.version import Version

from manage_django_project import __version__
from manage_django_project.config import project_info
from manage_django_project.management.commands import code_style


class ProjectSettingsTestCase(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        project_info.assert_initialized()

    def test_version(self):
        self.assertIsInstance(project_info.module_version, Version)
        self.assertIsInstance(project_info.config.module, ModuleType)

        self.assertEqual(project_info.module_version, Version(project_info.config.module.__version__))

        self.assertIsNotNone(__version__)
        version = Version(__version__)
        self.assertEqual(project_info.module_version, version)

    def test_code_style(self):
        # Just run our django manage command that call's ruff

        try:
            call_command(code_style.Command())
        except SystemExit as err:
            if err.code != 0:
                self.fail('Code style errors, see above!')

    def test_check_editor_config(self):
        check_editor_config(package_root=project_info.config.project_root_path)

        max_line_length = get_py_max_line_length(package_root=project_info.config.project_root_path)
        self.assertEqual(max_line_length, 119)
