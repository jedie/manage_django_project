"""
    Just "Overwrite" the existing manage_django_project/management/commands/publish.py
    because we would like to publish "manage_django_project"
    and not "manage_django_project_example"
"""
from manageprojects.utilities.publish import publish_package

import manage_django_project
from manage_django_project.config import project_info
from manage_django_project.management.commands.publish import Command as OriginPublishCommand


class Command(OriginPublishCommand):
    def publish(self):
        publish_package(
            module=manage_django_project,  # <<< set the correct module!
            package_path=project_info.config.project_root_path,
        )
