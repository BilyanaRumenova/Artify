from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client

from artify.art_items.models import ArtItem
from tests.base.mixins import ArtItemTestUtils, UserTestUtils
from tests.base.tests import ArtifyTestCase

UserModel = get_user_model()


class CreateNewArtItemTest(ArtItemTestUtils, UserTestUtils, ArtifyTestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(
            email='bilyana@test.bg',
            password='test1234'
        )
        self.art_item = self.create_item(
            type='fashion',
            name='test',
            description='test item description',
            image='path/to/image.png',
            user=self.user,
        )

    def test_createItemWhenNotSignedIn__shouldRaiseError(self):
        response = self.client.get(reverse('create item'), follow=True)
        self.assertEqual(404, response.status_code)

    def test_createItemWhenSignedInWithValidData__shouldCreateItem(self):
        self.client.login()
        response = self.client.get(reverse('create item'))

        art_item = self.art_item

        self.assertTrue(art_item.full_clean)
        self.assertEqual(302, response.status_code)
        self.assertEqual('test', art_item.name)

    def test_createItemWhenSignedInWithTooShortName__shouldNotCreateItem(self):
        self.client.login()
        response = self.client.get(reverse('create item'))

        art_item = self.create_item(
            type='fashion',
            name='1',
            description='test item description',
            image='path/to/image.png',
            user=self.user,
        )

        self.assertRaises(ValidationError, art_item.full_clean)
        self.assertEqual(302, response.status_code)

    def test_createItemWhenSignedInWithTooLongName__shouldNotCreateItem(self):
        self.client.login()

        with self.assertRaises(ValidationError):
            art_item = ArtItem(
                type='fashion',
                name='test test test test test test test test test ',
                description='test item description',
                image='path/to/image.png',
                user=self.user,
            )
            art_item.full_clean()
        response = self.client.get(reverse('create item'))
        self.assertEqual(302, response.status_code)

    def test_createItemWhenSignedInWithInvalidType__shouldNotCreateItem(self):
        self.client.login()

        with self.assertRaises(ValidationError):
            art_item = ArtItem(
                type='other',
                name='test',
                description='test item description',
                image='path/to/image.png',
                user=self.user,
            )
            art_item.full_clean()
        response = self.client.get(reverse('create item'))
        self.assertEqual(302, response.status_code)

    def test_createItemWhenSignedInWithInvalidDescription__shouldNotCreateItem(self):
        self.client.login()

        with self.assertRaises(ValidationError):
            art_item = ArtItem(
                type='other',
                name='test',
                description='invalid description invalid description invalid description invalid description '
                            'invalid description invalid description invalid description invalid description ',
                image='path/to/image.png',
                user=self.user,
            )
            art_item.full_clean()
        response = self.client.get(reverse('create item'))
        self.assertEqual(302, response.status_code)

    def test_createItemWhenSignedInWithInvalidImagePath__shouldNotCreateItem(self):
        self.client.login()

        with self.assertRaises(ValidationError):
            art_item = ArtItem(
                type='other',
                name='test',
                description='description ',
                image='abvg',
                user=self.user,
            )
            art_item.full_clean()
        response = self.client.get(reverse('create item'))
        self.assertEqual(302, response.status_code)












