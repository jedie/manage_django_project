from cli_base.cli_tools.subprocess_utils import verbose_check_call

from manage_django_project.config import project_info
from manage_django_project.management.base import BaseManageCommand


class Command(BaseManageCommand):
    help = 'Just install the project as editable via pip (Useful if version has been changed)'

    def handle(self, *args, **options):
        verbose_check_call('pip', 'install', '--no-deps', '-e', '.', cwd=project_info.config.project_root_path)
