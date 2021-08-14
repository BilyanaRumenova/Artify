from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse

from artify.accounts.models import ArtifyUser

UserModel = get_user_model()


class Authentication(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = ArtifyUser.objects.create_user(email='bilyana@test.bg', password='test1234')

    def test_signUpWithValidCredentials__shouldCreateUser(self):
        response = self.client.post(reverse('sign up user'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.is_authenticated)
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_signUpWithInvalidCredentials__shouldNotCreateUser(self):
        with self.assertRaises(ValidationError):
            user = ArtifyUser.objects.create_user(email='bilyaestbg', password='test1234')
            user.full_clean()
            self.assertTrue(self.user.is_authenticated)

        response = self.client.post(reverse('sign up user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_signInWhenValidCredentials__ShouldSignIn(self):
        response = self.client.post(reverse('sign in user'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.is_authenticated)
        self.assertTemplateUsed(response, 'accounts/signin.html')

    def test_signInWhenInvalidCredentials__ShouldNotSignIn(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        response = self.client.post(reverse('sign in user'), self.credentials)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signin.html')

    def test_sign_out(self):
        self.client.force_login(self.user)
        self.assertTrue(self.user.is_authenticated)

        response = self.client.get(reverse('sign out user'))
        self.assertEquals(response.status_code, 302)



