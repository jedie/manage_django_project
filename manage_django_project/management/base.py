from django_rich.management import RichCommand
from rich.panel import Panel

from manage_django_project.config import project_info


class PrintHelpMixin:
    help = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        assert self.help is not None, 'Help must be set in sub class!'
        self._help_printed = False

    def print_help_once(self):
        if not self._help_printed:
            self.console.print(Panel(f'[bold]{self.help}'))

        self._help_printed = True


class BaseManageCommand(PrintHelpMixin, RichCommand):

    def execute(self, *args, **options):
        if options['verbosity']:
            self.print_help_once()

        project_info.assert_initialized()

        super().execute(*args, **options)


class BasePassManageCommand(PrintHelpMixin, RichCommand):
    help = ''

    def run_from_argv(self, argv):
        self.print_help_once()
