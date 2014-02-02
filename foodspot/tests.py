from django.test import TestCase


class HomeViewTest(TestCase):
    url = '/'

    def test_renders_template(self):
        resp = self.client.get(self.url)
        self.assertTemplateUsed(resp, 'home.html')