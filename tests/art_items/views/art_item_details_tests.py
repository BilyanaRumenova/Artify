from django.urls import reverse

from artify.art_items.models import ArtItem, Like
from tests.base.mixins import ArtItemTestUtils, UserTestUtils
from tests.base.tests import ArtifyTestCase


class ArtItemDetailsTest(ArtItemTestUtils, UserTestUtils, ArtifyTestCase):

    def test_getArtItemDetails_whenArtItemDoesNotExistsAndIsOwner_shouldReturnDetailsForOwner(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('item details', kwargs={
            'pk': 4,
        }))
        self.assertEqual(404, response.status_code)
        self.assertFalse(ArtItem.objects.filter(name='test').exists())

    def test_getArtItemDetails_whenArtItemExistsAndIsOwnerAndNotLiked_shouldReturnDetailsForOwner(self):
        self.client.force_login(self.user)
        item = self.create_item(
            type=ArtItem.TYPE_CHOICE_PORTRAIT,
            name='Test Art Item',
            description='Test item description',
            image='path/to/image.png',
            user=self.user,
        )

        response = self.client.get(reverse('item details', kwargs={
            'pk': item.id,
        }))

        self.assertTrue(response.context['is_owner'])
        self.assertFalse(response.context['is_liked'])
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'art_items/item-details.html')

    def test_getArtItemDetails_whenArtItemExistsAndIsNotOwnerAndNotLiked_shouldReturnDetailsForOwner(self):
        self.client.force_login(self.user)
        item_user = self.create_user(email='item@user.com', password='1234test')
        item = self.create_item(
            type=ArtItem.TYPE_CHOICE_PORTRAIT,
            name='Test Art Item',
            description='Test item description',
            image='path/to/image.png',
            user=item_user,
        )

        response = self.client.get(reverse('item details', kwargs={
            'pk': item.id,
        }))

        self.assertFalse(response.context['is_owner'])
        self.assertFalse(response.context['is_liked'])
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'art_items/item-details.html')


    def test_getArtItemDetails_whenArtExistsAndIsNotOwnerAndLiked_shouldReturnDetailsForOwner(self):
        self.client.force_login(self.user)
        item_user = self.create_user(email='item@user.com', password='12345qwe')
        item = self.create_item_with_like(
            like_user=self.user,
            type=ArtItem.TYPE_CHOICE_PORTRAIT,
            name='Test Art Item',
            description='Test item description',
            image='path/to/image.png',
            user=item_user,
        )

        response = self.client.get(reverse('item details', kwargs={
            'pk': item.id,
        }))

        self.assertFalse(response.context['is_owner'])
        self.assertTrue(response.context['is_liked'])
        self.assertTemplateUsed(response, 'art_items/item-details.html')
