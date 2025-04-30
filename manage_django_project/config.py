import dataclasses
import logging
import tomllib
from importlib import import_module
from importlib.util import find_spec
from pathlib import Path
from types import ModuleType

from bx_py_utils.path import assert_is_file
from packaging.version import Version

from manage_django_project.exceptions import ConfigKeyError, ModuleNotFound, SettingsNotFound


logger = logging.getLogger(__name__)


@dataclasses.dataclass
class ManageConfig:
    module: ModuleType
    project_root_path: Path

    # dotted name of Django settings for...
    local_settings: str  # ... run local Django dev. server
    test_settings: str  # ... run tests

    # All Django manage commands that should use the "test" settings, instead of "local" settings:
    test_settings_commands: tuple = ('test', 'coverage', 'nox', 'update_test_snapshot_files')

    def __post_init__(self):
        for attr_name in ('local_settings', 'test_settings'):
            settings_str = getattr(self, attr_name)
            try:
                spec = find_spec(settings_str)
                assert spec, f'Settings "{settings_str}" can not import: Not found!'
            except (ModuleNotFoundError, AssertionError) as err:
                raise SettingsNotFound(f'{err} (Hint: Check "{attr_name}" in your pyproject.toml !)')


def read_pyproject_toml(path: Path) -> dict:
    assert_is_file(path)
    pyproject_toml = tomllib.loads(path.read_text(encoding='UTF-8'))
    return pyproject_toml


class NoPyprojectTomlFound(FileNotFoundError):
    pass


def detect_pyproject_toml() -> Path:
    path = Path.cwd()
    for _ in range(100):
        candidate = path / 'pyproject.toml'
        if candidate.is_file():
            return candidate

        if len(path.parts) > 1:
            # Look in parent direcotry
            path = path.parent
        else:
            # we are in root directory -> don't look further
            break

    raise NoPyprojectTomlFound(f'No "pyproject.toml" found from cwd {Path.cwd()}')


def get_config() -> ManageConfig:
    """
    Init and return ManageConfig from settings in pyproject.toml
    """
    pyproject_toml_path = detect_pyproject_toml()
    pyproject_toml = read_pyproject_toml(path=pyproject_toml_path)
    assert pyproject_toml, f'No data from: {pyproject_toml_path}'

    try:
        toml_cfg = pyproject_toml['manage_django_project']
        module_name = toml_cfg['module_name']
        local_settings = toml_cfg['local_settings']
        test_settings = toml_cfg['test_settings']
    except KeyError as err:
        raise ConfigKeyError(f'No {err} in {pyproject_toml_path}')

    assert module_name, f'Config value "module_name" is empty in {pyproject_toml_path}'
    assert local_settings, f'Config value "local_settings" is empty in {pyproject_toml_path}'
    assert test_settings, f'Config value "test_settings" is empty in {pyproject_toml_path}'

    try:
        module = import_module(module_name)
    except Exception as err:
        raise ModuleNotFound(f'{err} (Hint: Check {module_name=} in {pyproject_toml_path}')

    config = ManageConfig(
        module=module,
        project_root_path=pyproject_toml_path.parent,
        local_settings=local_settings,
        test_settings=test_settings,
    )
    return config


@dataclasses.dataclass
class ProjectInfo:
    initialized: bool = False

    config: ManageConfig = None
    pyproject_toml_path: Path | None = None
    distribution_name: str | None = None
    module_version: Version | None = None

    def initialize(self):
        if self.initialized:
            logger.info('Already initialized')
            return

        self.config = get_config()

        self.module_version = Version(self.config.module.__version__)
        self.pyproject_toml_path = Path(self.config.project_root_path, 'pyproject.toml')

        pyproject_toml = self.get_pyproject_toml()
        self.distribution_name = pyproject_toml['project']['name']

        self.initialized = True

    def assert_initialized(self):
        assert self.initialized is True, f'Not initialized: {self}'

    def get_pyproject_toml(self) -> dict:
        return read_pyproject_toml(path=self.pyproject_toml_path)

    def get_settings_by_command(self, *, command_name) -> str:
        if command_name in self.config.test_settings_commands:
            return self.config.test_settings

        return self.config.local_settings

    def get_current_settings(self, argv) -> str | None:
        for arg in argv:
            if arg.startswith('--settings'):
                # e.g.: Start a manage command with --settings option -> don't force any settings
                return

        if len(argv) > 1:
            settings_name = self.get_settings_by_command(command_name=argv[1])
        else:
            settings_name = self.config.local_settings

        return settings_name


project_info = ProjectInfo()
