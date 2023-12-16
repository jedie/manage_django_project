import os
import sys
import warnings

from cli_base.cli_tools.version_info import print_version
from rich import print

from manage_django_project.config import ManageConfig, project_info


def execute_django_from_command_line(*, config: ManageConfig = None, argv=None):
    if config is not None:
        warnings.warn(
            'config argument for execute_django_from_command_line() is deprecated and will removed in the future!',
            DeprecationWarning,
            stacklevel=2,
        )

    if argv is None:
        argv = sys.argv

    if len(argv) == 1:
        # Go into cmd2 shell if no command are given:
        argv.append('shell')

    project_info.initialize()

    print_version(module=project_info.config.module, project_root=project_info.config.project_root_path)
    print()

    if 'DJANGO_SETTINGS_MODULE' not in os.environ:
        if DJANGO_SETTINGS_MODULE := project_info.get_current_settings(argv):
            print(f'Set {DJANGO_SETTINGS_MODULE=}', file=sys.stderr)
            os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_SETTINGS_MODULE
        else:
            print('(Do not set DJANGO_SETTINGS_MODULE)')
    else:
        print(f'DJANGO_SETTINGS_MODULE={os.environ["DJANGO_SETTINGS_MODULE"]}', file=sys.stderr)

    print()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            'Couldn\'t import Django. Are you sure it\'s installed and '
            'available on your PYTHONPATH environment variable? Did you '
            'forget to activate a virtual environment?'
        ) from exc
    try:
        execute_from_command_line(argv)
    except Exception as err:
        from bx_py_utils.error_handling import print_exc_plus

        print_exc_plus(err, max_chars=400)
        raise
