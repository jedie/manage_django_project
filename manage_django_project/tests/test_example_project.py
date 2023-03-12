from django.conf import settings
from django.test import TestCase


class ExampleProjectTestCase(TestCase):
    def test_settings(self):
        self.assertEqual(settings.SETTINGS_MODULE, 'manage_django_project_example.settings.tests')

    def test_index_page(self):
        response = self.client.get('/')
        self.assertRedirects(response, expected_url='/login/?next=/')
