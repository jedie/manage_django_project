from django.apps import AppConfig


class ExampleProjectAppConfig(AppConfig):
    name = 'manage_django_project_example'
    verbose_name = 'Example Project'

    def ready(self):
        import manage_django_project_example.checks  # noqa
