import sys
from pathlib import Path
from typing import Optional

from bx_py_utils.path import assert_is_file
from django_rich.management import RichCommand
from manageprojects.utilities.pyproject_toml import find_pyproject_toml
from manageprojects.utilities.subprocess_utils import verbose_check_call


try:
    import tomllib  # New in Python 3.11
except ImportError:
    try:
        import tomli as tomllib
    except ImportError as err:
        raise ImportError(f'Please add "tomli" to your dev-dependencies! Origin error: {err}')


class NoPyProjectTomlFound(FileNotFoundError):
    pass


def get_pyproject_toml(*, file_path: Optional[Path] = None) -> dict:
    # TODO: Move to manageprojects
    if not file_path:
        file_path = Path.cwd()
    pyproject_toml_path = find_pyproject_toml(file_path=file_path)
    if not pyproject_toml_path:
        raise NoPyProjectTomlFound(f'Can not find "pyproject.toml" in {file_path}')

    assert_is_file(pyproject_toml_path)

    pyproject_text = pyproject_toml_path.read_text(encoding="utf-8")
    pyproject_config = tomllib.loads(pyproject_text)
    return pyproject_config


class Command(RichCommand):
    help = 'Update project requirements via pip-tools'

    def handle(self, *args, **options):
        self.console.print(f'\n[bold]{self.help}')
        verbose = options['verbosity'] > 1

        pyproject_config = get_pyproject_toml()
        project_cfg = pyproject_config['project']
        assert 'dependencies' in project_cfg, 'No "dependencies" in [project] in "pyproject.toml" found!'

        bin_path = Path(sys.executable).parent

        verbose_check_call(bin_path / 'pip', 'install', '-U', 'pip')
        verbose_check_call(bin_path / 'pip', 'install', '-U', 'pip-tools')

        extra_env = dict(
            CUSTOM_COMPILE_COMMAND='./manage.py update_req',
        )

        pip_compile_base = [
            bin_path / 'pip-compile',
            '--allow-unsafe',  # https://pip-tools.readthedocs.io/en/latest/#deprecations
            '--resolver=backtracking',  # https://pip-tools.readthedocs.io/en/latest/#deprecations
            '--upgrade',
            '--generate-hashes',
        ]
        if verbose:
            pip_compile_base.append('--verbose')

        # Only "prod" dependencies:
        verbose_check_call(
            *pip_compile_base,
            'pyproject.toml',
            '--output-file',
            'requirements.txt',
            extra_env=extra_env,
        )
        last_requirements_name = 'requirements.txt'

        if opt_deps := pyproject_config['project'].get('optional-dependencies'):
            opt_dep_names = opt_deps.keys()
            if opt_dep_names:
                assert 'dev' in opt_dep_names, 'No "dev" list in [project.optional-dependencies] found!'
                for name in opt_dep_names:
                    requirements_name = f'requirements.{name}.txt'
                    verbose_check_call(
                        *pip_compile_base,
                        'pyproject.toml',
                        '--extra=dev',
                        f'--extra={name}',
                        '--output-file',
                        requirements_name,
                        extra_env=extra_env,
                    )
                    last_requirements_name = requirements_name

        # Install new dependencies in current .venv:
        verbose_check_call('pip-sync', last_requirements_name)
