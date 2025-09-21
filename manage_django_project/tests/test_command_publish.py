from unittest.mock import patch

from django.core.management import call_command
from django.test import SimpleTestCase

import manage_django_project_example
from manage_django_project.management.commands import publish
from manage_django_project.tests import PROJECT_ROOT


class ConfigTestCase(SimpleTestCase):
    def test_basic(self):
        with patch.object(publish, 'publish_package') as publish_package_mock, patch.object(
            publish, 'verbose_check_call'
        ) as verbose_check_call_mock:
            call_command(publish.Command())
        publish_package_mock.assert_called_once_with(
            module=manage_django_project_example,
            package_path=PROJECT_ROOT,
            distribution_name='manage_django_project',
        )
        verbose_check_call_mock.assert_called_once_with(
            './manage.py',
            'test',
            extra_env={'DJANGO_SETTINGS_MODULE': 'manage_django_project_example.settings.tests'},
        )
