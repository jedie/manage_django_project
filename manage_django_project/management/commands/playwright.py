import sys

from manage_django_project.management.base import BasePassManageCommand


class Command(BasePassManageCommand):
    help = 'Call playwright CLI'

    def run_from_argv(self, argv):
        super().run_from_argv(argv)

        try:
            from playwright.__main__ import main
        except ImportError as err:
            self.stderr.write(f'No playwright installed? (Origin error: {err})')
        else:
            sys.argv = sys.argv[1:]
            main()
