from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from artify.art_items.models import ArtItem
from tests.base.mixins import ArtItemTestUtils, UserTestUtils
from tests.base.tests import ArtifyTestCase

UserModel = get_user_model()


class DeleteArtItemTest(ArtItemTestUtils, UserTestUtils, ArtifyTestCase):
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

    def test_getRequestToDeleteArtItemWhenOwner__shouldReturnDeletePage(self):
        self.client.force_login(self.user)
        art_item = self.art_item
        response = self.client.get(reverse('delete item', kwargs={
            'pk': art_item.id,
        }))
        self.assertContains(response, 'Are you sure you want to delete')

    def test_postRequestToDeleteArtItemWhenOwner__shouldDeleteArtItem(self):
        self.client.force_login(self.user)
        post_response = self.client.post(reverse('delete item', kwargs={
            'pk': self.art_item.id,
        }))
        self.assertRedirects(post_response, reverse('list items'), status_code=302)

    def test_deleteArtItemWhenArtItemDoesNotExist__shouldRaiseError(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('delete item', kwargs={
            'pk': 4,
        }))
        self.assertEqual(404, response.status_code)
        self.assertFalse(ArtItem.objects.filter(id=4).exists())

    def test_deleteArtItemWhenNotOwner__shouldRaiseError(self):
        self.client.force_login(self.user)
        guest_user = UserModel.objects.create_user(
            email='bilyana56@test.bg',
            password='test123456'
        )
        art_item = self.create_item(
            type='fashion',
            name='test',
            description='test item description',
            image='path/to/image.png',
            user=guest_user,
        )
        response = self.client.get(reverse('delete item', kwargs={
            'pk': art_item.id,
        }))
        self.assertEqual(403, response.status_code)


