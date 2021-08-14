from django.test import TestCase, Client
from django.urls import reverse


class TestLandingPage(TestCase):

    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')

    def test_landing_page_whenNotSignedIn(self):
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing_page.html')

    def test_landing_page_whenSignedIn(self):
        self.client.login()
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing_page.html')