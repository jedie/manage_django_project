from cli_base.cli_tools.subprocess_utils import verbose_check_call
from manageprojects.utilities import code_style

from manage_django_project.config import project_info
from manage_django_project.management.base import BaseManageCommand


class Command(BaseManageCommand):
    help = 'Check/Fix project code style'

    def handle(self, *args, **options):
        verbose = options['verbosity'] > 1
        color = not options['no_color']

        project_root_path = project_info.config.project_root_path

        code_style._call_darker(package_root=project_root_path, color=color, verbose=verbose)
        verbose_check_call(
            'flake8',
            *args,
            cwd=project_root_path,
            exit_on_error=True,
        )
        print('Code style: OK')
