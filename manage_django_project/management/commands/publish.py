from cli_base.cli_tools.subprocess_utils import verbose_check_call
from manageprojects.utilities.publish import publish_package
from rich.pretty import pprint

from manage_django_project.config import project_info
from manage_django_project.management.base import BaseManageCommand


class Command(BaseManageCommand):
    help = 'Build a new release and publish it to PyPi'

    def handle(self, *args, **options):
        # don't publish if tests fail:
        verbose_check_call(
            './manage.py',
            'test',
            extra_env=dict(  # Use the test settings:
                DJANGO_SETTINGS_MODULE=project_info.config.test_settings,
            ),
        )
        # test pass -> publish:
        self.publish()

    def publish(self):
        kwargs = dict(
            module=project_info.config.module,
            package_path=project_info.config.project_root_path,
            distribution_name=project_info.distribution_name,
        )
        print('Start publishing with:')
        pprint(kwargs)
        publish_package(**kwargs)
