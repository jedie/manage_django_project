import sys

from manage_django_project.management.base import BasePassManageCommand, ManageDjangoToolsExecutor
from manage_django_project.management.commands.coverage import coverage_combine_report, erase_coverage_data


class Command(BasePassManageCommand):
    help = 'Run tests via nox'

    def run_from_argv(self, argv):
        super().run_from_argv(argv)

        tools_executor = ManageDjangoToolsExecutor()

        try:
            # Just pass every argument to the origin nox CLI:
            tools_executor.verbose_check_call('nox', *argv[2:], exit_on_error=True)
            coverage_combine_report(verbose=True)
        finally:
            # Always remove coverage data files, after test run:
            erase_coverage_data(verbose=False)

        sys.exit(0)
