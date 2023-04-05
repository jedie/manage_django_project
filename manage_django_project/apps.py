from django.apps import AppConfig

from manage_django_project.config import project_info


class ManageDjangoProjectConfig(AppConfig):
    name = "manage_django_project"
    verbose_name = "Manage Django Project"

    def ready(self):
        project_info.initialize()
        project_info.assert_initialized()
