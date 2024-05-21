from cli_base.cli_tools.subprocess_utils import verbose_check_call
from django_rich.management import RichCommand


class Command(RichCommand):
    help = 'Run safety check against current requirements files'

    def handle(self, *args, **options):
        self.console.print(f'\n[bold]{self.help}')

        verbose_check_call(
            'safety',
            'check',
            '-r',
            'requirements.dev.txt',
            '--ignore',
            '67599',  # Ignore CVE-2018-20225: We do not use the `--extra-index-url` option
        )
