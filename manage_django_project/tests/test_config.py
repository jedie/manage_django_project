import inspect
import logging
import os
import tempfile
from pathlib import Path

from bx_py_utils.path import assert_is_file
from django.test import SimpleTestCase

import manage_django_project_example
from manage_django_project.config import (
    ManageConfig,
    NoPyprojectTomlFound,
    detect_pyproject_toml,
    get_config,
    project_info,
    read_pyproject_toml,
)
from manage_django_project.exceptions import ConfigKeyError, ModuleNotFound, SettingsNotFound


logger = logging.getLogger(__name__)


class TemporaryWorkDirectory:
    def __init__(self, prefix=None):
        self.prefix = prefix
        self.old_cwd = Path.cwd()

    def __enter__(self) -> Path:
        temp_name = tempfile.mkdtemp(prefix=self.prefix)
        self.temp_path = Path(temp_name)
        os.chdir(self.temp_path)
        return self.temp_path

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.old_cwd)


class ConfigTestCase(SimpleTestCase):
    def test_basic(self):
        project_info.assert_initialized()

        self.assertEqual(project_info.distribution_name, 'manage_django_project')
        self.assertIsInstance(project_info.config, ManageConfig)
        self.assertEqual(project_info.config.module, manage_django_project_example)

    def test_detect_pyproject_toml(self):
        pyproject_toml_path = detect_pyproject_toml()
        assert_is_file(pyproject_toml_path)
        self.assertEqual(pyproject_toml_path.name, 'pyproject.toml')

        with TemporaryWorkDirectory(prefix='test_detect_pyproject_toml') as temp_path:
            with self.assertRaisesMessage(NoPyprojectTomlFound, f'No "pyproject.toml" found from cwd {temp_path}'):
                detect_pyproject_toml()

    def test_read_pyproject_toml(self):
        pyproject_toml = read_pyproject_toml(path=project_info.pyproject_toml_path)
        self.assertIsInstance(pyproject_toml, dict)
        self.assertEqual(pyproject_toml['project']['name'], 'manage_django_project')

    def test_manage_config(self):
        with self.assertRaisesMessage(
            SettingsNotFound,
            'Settings "wrong_local_settings" can not import: Not found!'
            ' (Hint: Check "local_settings" in your pyproject.toml !)',
        ):
            ManageConfig(
                module=project_info.config.module,
                project_root_path=project_info.config.project_root_path,
                local_settings='wrong_local_settings',
                test_settings=project_info.config.test_settings,
            )
        with self.assertRaisesMessage(
            SettingsNotFound,
            'No module named \'notexisting\' (Hint: Check "test_settings" in your pyproject.toml !)',
        ):
            ManageConfig(
                module=project_info.config.module,
                project_root_path=project_info.config.project_root_path,
                local_settings=project_info.config.local_settings,
                test_settings='notexisting.foo.bar',
            )

    def test_get_config(self):
        config = get_config()
        self.assertIsInstance(config, ManageConfig)
        self.assertEqual(config, project_info.config)

        with TemporaryWorkDirectory(prefix='test_get_config') as temp_path:
            test_toml = temp_path / 'pyproject.toml'
            test_toml.touch()

            with self.assertRaisesMessage(AssertionError, f'No data from: {test_toml}'):
                get_config()

            test_toml.write_text(
                inspect.cleandoc(
                    '''
                    [foo]
                    bar=1
                    '''
                )
            )

            with self.assertRaisesMessage(ConfigKeyError, "No 'manage_django_project' "):
                get_config()

            test_toml.write_text(
                inspect.cleandoc(
                    '''
                    [manage_django_project]
                    bar=1
                    '''
                )
            )
            with self.assertRaisesMessage(ConfigKeyError, "No 'module_name' "):
                get_config()

            test_toml.write_text(
                inspect.cleandoc(
                    '''
                    [manage_django_project]
                    module_name="foobar"
                    local_settings="foobar"
                    test_settings="foobar"
                    '''
                )
            )
            with self.assertRaisesMessage(ModuleNotFound, "No module named 'foobar' (Hint: Check module_name"):
                get_config()
