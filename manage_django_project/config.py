import dataclasses
from pathlib import Path
from types import ModuleType
from typing import Optional

from bx_py_utils.path import assert_is_file
from packaging.version import Version

from manage_django_project.management import commands


try:
    import tomllib  # New in Python 3.11
except ImportError:
    import tomli as tomllib


def get_own_commands():
    commands_path = Path(commands.__file__).parent
    own_commands = [item.stem for item in commands_path.glob('*.py') if not item.stem.startswith('_')]
    return own_commands


@dataclasses.dataclass
class ManageConfig:
    module: ModuleType
    project_root_path: Path

    # dotted name of Django settings for...
    prod_settings: str  # ... production
    local_settings: str  # ... run local Django dev. server
    test_settings: str  # ... run tests


@dataclasses.dataclass
class ProjectInfo:
    initialized: bool = False

    config: ManageConfig = None
    pyproject_toml_path: Optional[Path] = None
    distribution_name: Optional[str] = None
    module_version: Optional[Version] = None

    def initialize(self, config: ManageConfig):
        self.config = config

        self.module_version = Version(self.config.module.__version__)
        self.pyproject_toml_path = Path(self.config.project_root_path, 'pyproject.toml')

        pyproject_toml = self.get_pyproject_toml()
        self.distribution_name = pyproject_toml['project']['name']

        self.initialized = True

    def assert_initialized(self):
        assert self.initialized is True, f'No initialized: {self}'

    def get_pyproject_toml(self) -> dict:
        assert_is_file(self.pyproject_toml_path)
        pyproject_toml = tomllib.loads(self.pyproject_toml_path.read_text(encoding='UTF-8'))
        return pyproject_toml

    def get_current_settings(self, argv):
        settings_name = self.config.prod_settings

        if len(argv) == 1:
            # e.g.: just start "./manage.py" to display the --help page:
            settings_name = self.config.local_settings
        elif len(argv) > 1:
            command = argv[1]
            own_commands = get_own_commands()

            if command in own_commands:
                settings_name = self.config.local_settings

            if command in ('test', 'coverage', 'tox'):
                settings_name = self.config.test_settings

        return settings_name


project_info = ProjectInfo()
