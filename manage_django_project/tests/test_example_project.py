from django.test import TestCase


class ExampleProjectTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get('/')
        self.assertRedirects(response, expected_url='/login/?next=/')
