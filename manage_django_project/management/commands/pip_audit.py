from cli_base.run_pip_audit import run_pip_audit
from django_rich.management import RichCommand


class Command(RichCommand):
    help = 'Run `pip-audit` with configuration from `pyproject.toml`'

    def handle(self, *args, **options):
        self.console.print(f'\n[bold]{self.help}')

        run_pip_audit(verbosity=options['verbosity'])
