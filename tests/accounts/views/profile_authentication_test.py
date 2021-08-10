from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from artify.accounts.models import ArtifyUser

UserModel = get_user_model()


class Authentication(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = ArtifyUser.objects.create_user(email='bilyana@test.bg', password='test1234')

    def test_sign_up(self):
        response = self.client.post(reverse('sign up user'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.is_authenticated)

    def test_sign_in(self):
        response = self.client.post(reverse('sign in user'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.is_authenticated)

    def test_sign_out(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('index'))
        self.assertTrue(self.user.is_authenticated)
        self.assertEquals(response.status_code, 200)

        self.client.logout()
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)


