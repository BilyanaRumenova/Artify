from django.contrib.auth import get_user_model
from django.urls import reverse

from artify.art_items.models import ArtItem, Like
from tests.base.mixins import ArtItemTestUtils, UserTestUtils
from tests.base.tests import ArtifyTestCase

UserModel = get_user_model()


class LikeArtItemViewTests(ArtItemTestUtils, UserTestUtils, ArtifyTestCase):

    def test_likeArtItem__whenArtItemNotLiked(self):
        self.client.force_login(self.user)
        item_user = self.create_user(email='item@user.bg', password='1234test')
        item = self.create_item(
            type=ArtItem.TYPE_CHOICE_PORTRAIT,
            name='Test Art Item',
            description='Test item description',
            image='path/to/image.png',
            user=item_user,
        )
        response = self.client.get(reverse('like item', kwargs={'pk': item.id}))

        self.assertEqual(302, response.status_code)

        like_exists = Like.objects.filter(
            user_id=self.user.id,
            item_id=item.id
        ).exists()
        self.assertTrue(like_exists)

    def test_likeArtItem__whenArtItemAlreadyLiked(self):
        self.client.force_login(self.user)
        item_user = self.create_user(email='item@user.bg', password='1234test')
        item = self.create_item_with_like(
            like_user=self.user,
            type=ArtItem.TYPE_CHOICE_PORTRAIT,
            name='Test Art Item',
            description='Test item description',
            image='path/to/image.png',
            user=item_user,
        )
        response = self.client.get(reverse('like item', kwargs={'pk': item.id}))

        self.assertEqual(302, response.status_code)

        like_exists = Like.objects.filter(
            user_id=self.user.id,
            item_id=item.id
        ).exists()
        self.assertFalse(like_exists)


