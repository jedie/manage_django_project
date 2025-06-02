from cli_base.run_pip_audit import run_pip_audit
from django_rich.management import RichCommand

from manage_django_project.config import project_info
from manage_django_project.management.base import ManageDjangoToolsExecutor


class Command(RichCommand):
    help = 'Update project requirements via uv'

    def handle(self, *args, **options):
        self.console.print(f'\n[bold]{self.help}')
        verbosity = options['verbosity']

        project_root_path = project_info.config.project_root_path

        tools_executor = ManageDjangoToolsExecutor()

        tools_executor.verbose_check_call('pip', 'install', '-U', 'pip')
        tools_executor.verbose_check_call('pip', 'install', '-U', 'uv')
        tools_executor.verbose_check_call('uv', 'lock', '--upgrade')

        run_pip_audit(base_path=project_root_path, verbosity=verbosity)

        # Install new dependencies in current .venv:
        tools_executor.verbose_check_call('uv', 'sync')

        if tools_executor.is_executable('pre-commit'):
            # Update git pre-commit hooks:
            tools_executor.verbose_check_call('pre-commit', 'autoupdate')
