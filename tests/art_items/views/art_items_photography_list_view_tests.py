from django.urls import reverse

from artify.art_items.models import ArtItem
from tests.base.mixins import ArtItemTestUtils, UserTestUtils
from tests.base.tests import ArtifyTestCase


class ArtItemPhotographyListViewTest(ArtItemTestUtils, UserTestUtils, ArtifyTestCase):

    def test_getPhotographyArtItemsListWhenNotSignedIn__shouldRaiseError(self):
        response = self.client.get(reverse('photography items'), follow=True)
        self.assertEqual(404, response.status_code)

    def test_getPhotographyArtItemsListWhenSignedIn__shouldReturnPhotographyPhotos(self):
        self.client.force_login(self.user)

        item_user_1 = self.create_user(email='item1@user.com', password='1234test1')
        item_1 = self.create_item(
            type=ArtItem.TYPE_CHOICE_PHOTOGRAPHY,
            name='Test Art Item 1',
            description='Test item description 1',
            image='path/to/image1.png',
            user=item_user_1,
        )

        item_user_2 = self.create_user(email='item2@user.com', password='1234test2')
        item_2 = self.create_item(
            type=ArtItem.TYPE_CHOICE_PHOTOGRAPHY,
            name='Test Art Item 2',
            description='Test item description 2',
            image='path/to/image2.png',
            user=item_user_2,
        )
        response = self.client.get(reverse('photography items'))

        self.assertIn(item_1, response.context['photography_items'])
        self.assertIn(item_2, response.context['photography_items'])
        self.assertEqual(2, len(response.context['photography_items']))

    def test_createAnotherTypeArtItemsListWhenSignedIn__shouldReturnEmptyPhotographyList(self):
        self.client.force_login(self.user)

        item_user_1 = self.create_user(email='item1@user.com', password='1234test1')
        item_1 = self.create_item(
            type=ArtItem.TYPE_CHOICE_PORTRAIT,
            name='Test Art Item 1',
            description='Test item description 1',
            image='path/to/image1.png',
            user=item_user_1,
        )

        item_user_2 = self.create_user(email='item2@user.com', password='1234test2')
        item_2 = self.create_item(
            type=ArtItem.TYPE_CHOICE_PAINTING,
            name='Test Art Item 2',
            description='Test item description 2',
            image='path/to/image2.png',
            user=item_user_2,
        )
        response = self.client.get(reverse('photography items'))

        self.assertNotIn(item_1, response.context['photography_items'])
        self.assertNotIn(item_2, response.context['photography_items'])
        self.assertEqual(0, len(response.context['photography_items']))

