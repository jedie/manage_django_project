from cli_base.cli_tools.code_style import assert_code_style

from manage_django_project.config import project_info
from manage_django_project.management.base import BaseManageCommand


class Command(BaseManageCommand):
    help = 'Check/Fix project code style'

    def handle(self, *args, **options):
        assert_code_style(
            package_root=project_info.config.project_root_path,
            verbose=options['verbosity'] > 1,
            sys_exit=True,
        )
        print('Code style: OK')
