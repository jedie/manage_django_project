from django.test import SimpleTestCase

import manage_django_project_example
from manage_django_project.config import ManageConfig, project_info


class ConfigTestCase(SimpleTestCase):
    def test_basic(self):
        project_info.assert_initialized()

        self.assertEqual(project_info.distribution_name, 'manage_django_project')
        self.assertIsInstance(project_info.config, ManageConfig)
        self.assertEqual(project_info.config.module, manage_django_project_example)
