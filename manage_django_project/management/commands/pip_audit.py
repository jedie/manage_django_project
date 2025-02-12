from cli_base.run_pip_audit import run_pip_audit
from django_rich.management import RichCommand

from manage_django_project.config import project_info


class Command(RichCommand):
    help = 'Run `pip-audit` with configuration from `pyproject.toml`'

    def handle(self, *args, **options):
        self.console.print(f'\n[bold]{self.help}')

        project_root_path = project_info.config.project_root_path

        run_pip_audit(verbosity=options['verbosity'], base_path=project_root_path)
