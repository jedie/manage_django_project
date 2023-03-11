from types import ModuleType

from django.core.management import call_command
from django.test import SimpleTestCase
from manageprojects.test_utils.project_setup import check_editor_config
from packaging.version import Version

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

        pyproject_toml = project_info.get_pyproject_toml()
        pyproject_version = pyproject_toml['project']['version']

        self.assertEqual(project_info.config.module.__version__, pyproject_version)

    def test_check_editor_config(self):
        check_editor_config(package_root=project_info.config.project_root_path)

    def test_code_style(self):
        # Just run our django manage command that call's darker and flake8

        try:
            call_command(code_style.Command())
        except SystemExit as err:
            if err.code != 0:
                self.fail('Code style errors, see above!')
