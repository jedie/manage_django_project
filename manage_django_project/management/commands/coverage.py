from manageprojects.utilities.subprocess_utils import verbose_check_call

from manage_django_project.config import project_info
from manage_django_project.management.base import BaseManageCommand


def coverage_combine_report(verbose):
    cwd = project_info.config.project_root_path
    verbose_check_call('coverage', 'combine', '--append', verbose=verbose, exit_on_error=True, cwd=cwd)
    verbose_check_call('coverage', 'report', verbose=verbose, exit_on_error=True, cwd=cwd)
    verbose_check_call('coverage', 'xml', verbose=verbose, exit_on_error=True, cwd=cwd)
    verbose_check_call('coverage', 'json', verbose=verbose, exit_on_error=True, cwd=cwd)


class Command(BaseManageCommand):
    help = 'Run tests with coverage and report'

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-processing",
            action="store_true",
            dest="no_processing",
            help='Run only coverage tests, but do not combine result and report',
        )
        parser.add_argument(
            "--context",
            help='The context label to record for this coverage run.',
        )

    def handle(self, *args, **options):
        cwd = project_info.config.project_root_path

        no_processing = options['no_processing']

        verbose = options['verbosity'] > 0

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
                raise  # No report if tests fails

        if not no_processing:
            coverage_combine_report(verbose)
