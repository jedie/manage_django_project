
from manage_django_project.management.base import BaseManageCommand, ManageDjangoToolsExecutor


class Command(BaseManageCommand):
    help = 'Just install the project as editable via pip (Useful if version has been changed)'

    def handle(self, *args, **options):
        tools_executor = ManageDjangoToolsExecutor()
        tools_executor.verbose_check_call('pip', 'install', '--no-deps', '-e', '.')
