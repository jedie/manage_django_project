import sys

from manageprojects.utilities.subprocess_utils import verbose_check_call

from manage_django_project.management.base import BasePassManageCommand
from manage_django_project.management.commands.coverage import coverage_combine_report


class Command(BasePassManageCommand):
    help = 'Run tests via tox'

    def run_from_argv(self, argv):
        super().run_from_argv(argv)

        # Just pass every argument to the origin tox CLI:
        verbose_check_call(sys.executable, '-m', 'tox', *argv[2:], exit_on_error=True)

        coverage_combine_report(verbose=True)

        sys.exit(0)
