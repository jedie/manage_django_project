import os

from cli_base.cli_tools.dev_tools import coverage_combine_report, erase_coverage_data

from manage_django_project.management.base import BaseManageCommand, ManageDjangoToolsExecutor


class Command(BaseManageCommand):
    help = 'Run tests with coverage and report'

    def add_arguments(self, parser):
        parser.add_argument(
            "--context",
            help='The context label to record for this coverage run.',
        )

    def handle(self, *args, **options):
        verbose = options['verbosity'] > 0

        inside_tox_run = 'TOX_ENV_NAME' in os.environ  # Is this coverage run inside tox call?

        tools_executor = ManageDjangoToolsExecutor()

        old_coverage_data = tools_executor.cwd / '.coverage'
        old_coverage_data.unlink(missing_ok=True)

        args = ['coverage', 'run']
        if context := options['context']:
            args.append('--context')
            args.append(context)

        try:
            tools_executor.verbose_check_call(*args, verbose=verbose, exit_on_error=True)
        except SystemExit as err:
            if err.code != 0:
                erase_coverage_data(cwd=tools_executor.cwd, verbose=verbose)
                raise  # No report if tests fails

        if not inside_tox_run:
            coverage_combine_report(cwd=tools_executor.cwd, verbose=verbose)
            erase_coverage_data(cwd=tools_executor.cwd, verbose=verbose)
