import sys
from pathlib import Path

from cli_base.cli_tools.subprocess_utils import verbose_check_call
from django_rich.management import RichCommand
from manageprojects.utilities.pyproject_toml import TomlDocument, get_pyproject_toml


class Command(RichCommand):
    help = 'Update project requirements via pip-tools'

    def handle(self, *args, **options):
        self.console.print(f'\n[bold]{self.help}')
        verbose = options['verbosity'] > 1

        toml_document: TomlDocument = get_pyproject_toml()
        self.console.print(f'Use: {toml_document.file_path}')

        pyproject_config = toml_document.doc.unwrap()  # TOMLDocument -> dict

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
        requirements_names = ['requirements.txt']
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
                    requirements_names.append(requirements_name)

        # Install new dependencies in current .venv:
        verbose_check_call('pip-sync', last_requirements_name)

        self.console.print('\n')
        self.console.print('-' * 100)
        self.console.print('[green]Generate requirement files:')
        for requirements_name in requirements_names:
            self.console.print(f'[bold] * [cyan]{requirements_name}')

        self.console.print(f'\n[green]Install requirement from: [bold]{last_requirements_name}\n')
