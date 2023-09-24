import os

from cli_base.cli_tools.subprocess_utils import verbose_check_call

from manage_django_project.config import project_info
from manage_django_project.management.base import BaseManageCommand


class EraseCoverageData:
    """Erase previously collected coverage data"""

    erased = False

    def __call__(self, verbose):
        if not self.erased:
            cwd = project_info.config.project_root_path
            verbose_check_call('coverage', 'erase', verbose=verbose, exit_on_error=True, cwd=cwd)
        self.erased = True  # Call only once at runtime!


erase_coverage_data = EraseCoverageData()


def coverage_combine_report(verbose):
    cwd = project_info.config.project_root_path
    verbose_check_call('coverage', 'combine', '--append', verbose=verbose, exit_on_error=True, cwd=cwd)
    verbose_check_call('coverage', 'report', verbose=verbose, exit_on_error=True, cwd=cwd)
    verbose_check_call('coverage', 'xml', verbose=verbose, exit_on_error=True, cwd=cwd)
    verbose_check_call('coverage', 'json', verbose=verbose, exit_on_error=True, cwd=cwd)
    erase_coverage_data(verbose=True)


class Command(BaseManageCommand):
    help = 'Run tests with coverage and report'

    def add_arguments(self, parser):
        parser.add_argument(
            "--context",
            help='The context label to record for this coverage run.',
        )

    def handle(self, *args, **options):
        cwd = project_info.config.project_root_path

        verbose = options['verbosity'] > 0

        inside_tox_run = 'TOX_ENV_NAME' in os.environ  # Is this coverage run inside tox call?

        old_coverage_data = cwd / '.coverage'
        old_coverage_data.unlink(missing_ok=True)

        args = ['coverage', 'run']
        if context := options['context']:
            args.append('--context')
            args.append(context)

        try:
            verbose_check_call(*args, verbose=verbose, exit_on_error=True, cwd=cwd)
        except SystemExit as err:
            if err.code != 0:
                erase_coverage_data(verbose=True)
                raise  # No report if tests fails

        if not inside_tox_run:
            coverage_combine_report(verbose)
            erase_coverage_data(verbose=True)
