from django.urls import reverse

from artify.art_items.models import ArtItem
from tests.base.mixins import ArtItemTestUtils, UserTestUtils
from tests.base.tests import ArtifyTestCase


class ArtItemListViewTest(ArtItemTestUtils, UserTestUtils, ArtifyTestCase):

    def test_getArtItemsList__shouldReturnAllPhotos(self):
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
            type=ArtItem.TYPE_CHOICE_FASHION,
            name='Test Art Item 2',
            description='Test item description 2',
            image='path/to/image2.png',
            user=item_user_2,
        )
        response = self.client.get(reverse('list items'))

        self.assertIn(item_1, response.context['art_items'])
        self.assertIn(item_2, response.context['art_items'])
        self.assertEqual(2, len(response.context['art_items']))

    def test_getArtItemsListWhenNotSignedIn__shouldRaiseError(self):
        response = self.client.get(reverse('list items'), follow=True)
        self.assertEqual(404, response.status_code)

