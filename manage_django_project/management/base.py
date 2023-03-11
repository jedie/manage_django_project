from django_rich.management import RichCommand

from manage_django_project.config import project_info


class BaseManageCommand(RichCommand):
    help = ''

    def execute(self, *args, **options):
        if options['verbosity']:
            self.console.print('_' * 100)
            self.console.print(f'[bold]{self.help}')

        project_info.assert_initialized()

        super().execute(*args, **options)


class BasePassManageCommand(RichCommand):
    help = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.console.print(f'\n[bold]{self.help}')
