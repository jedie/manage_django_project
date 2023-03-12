from manageprojects.utilities.publish import publish_package
from manageprojects.utilities.subprocess_utils import verbose_check_call

from manage_django_project.config import project_info
from manage_django_project.management.base import BaseManageCommand


class Command(BaseManageCommand):
    help = 'Build a new release and publish it to PyPi'

    def handle(self, *args, **options):
        verbose_check_call('./manage.py', 'test')  # don't publish if tests fail
        self.publish()

    def publish(self):
        publish_package(
            module=project_info.config.module,
            package_path=project_info.config.project_root_path,
        )
