from django.contrib.auth import get_user_model
from django.test import TestCase, Client

UserModel = get_user_model()


class ArtifyTestCase(TestCase):
    signed_in_user_email = 'bilyana@test.bg'
    signed_in_user_password = 'test1234'

    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(
            email=self.signed_in_user_email,
            password=self.signed_in_user_password,
        )