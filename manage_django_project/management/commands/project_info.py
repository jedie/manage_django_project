from rich.pretty import Pretty

from manage_django_project.config import project_info
from manage_django_project.management.base import BaseManageCommand


class Command(BaseManageCommand):
    help = 'Information about the current Django project'

    def handle(self, *args, **options):
        self.console.print('\nmanage_config = ', end='')
        self.console.print(Pretty(project_info))
