import sys

from manageprojects.utilities.subprocess_utils import verbose_check_call

from manage_django_project.management.base import BasePassManageCommand
from manage_django_project.management.commands.coverage import coverage_combine_report


class Command(BasePassManageCommand):
    help = 'Run tests via tox'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Just pass everything to the origin tox CLI:

        verbose_check_call(sys.executable, '-m', 'tox', *sys.argv[2:])

        coverage_combine_report(verbose=True)

        sys.exit(0)
