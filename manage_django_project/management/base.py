from django_rich.management import RichCommand

from manage_django_project.config import project_info


class BaseManageCommand(RichCommand):
    help = ''

    def execute(self, *args, **options):
        if options['verbosity']:
            self.console.print('_' * self.console.width)
            self.console.print(f'[bold]{self.help}')

        project_info.assert_initialized()

        super().execute(*args, **options)


class BasePassManageCommand(RichCommand):
    help = ''

    def run_from_argv(self, argv):
        self.console.print('_' * self.console.width)
        self.console.print(f'[bold]{self.help}')
