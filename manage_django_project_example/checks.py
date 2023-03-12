from django.conf import settings
from django.core.checks import Error, register


@register()
def check_settings(app_configs, **kwargs):
    errors = []
    if not settings.SETTINGS_MODULE.startswith('manage_django_project_example.settings.'):
        errors.append(
            Error(
                f'Wrong settings: {settings.SETTINGS_MODULE=} is not a manage_django_project_example settings',
                id='manage_django_project_example.E001',
            )
        )
    return errors
