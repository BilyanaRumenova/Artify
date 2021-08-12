import factory

from django.urls import reverse

from artify.accounts import signals
from artify.accounts.models import Profile
from artify.art_items.models import ArtItem, Follow
from tests.base.mixins import ArtItemTestUtils, UserTestUtils
from tests.base.tests import ArtifyTestCase


class ArtItemHomeViewTest(ArtItemTestUtils, UserTestUtils, ArtifyTestCase):

    @factory.django.mute_signals(signals.post_save)
    def test_getHomePageWithArtItemsList_whenFollowedProfileHasUploadedImage__shouldReturnFeed(self):
        self.client.force_login(self.user)

        followed_user = self.create_user(email='item1@user.com', password='1234test1')
        followed_profile = Profile.objects.create(
            first_name='test',
            user=followed_user
        )
        item_from_feed = self.create_item(
            type=ArtItem.TYPE_CHOICE_PORTRAIT,
            name='Test Art Item 1',
            description='Test item description 1',
            image='path/to/image1.png',
            user=followed_user,
        )
        Follow.objects.create(
            profile_to_follow=followed_profile,
            follower=self.user
        )

        response = self.client.get(reverse('home'))

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.context['feed']))
        self.assertIn(item_from_feed, response.context['feed'])

    @factory.django.mute_signals(signals.post_save)
    def test_getHomePageWithArtItemsList_whenFollowedProfileHasNotUploadedImage__shouldReturnEmptyFeed(self):
        self.client.force_login(self.user)

        followed_user = self.create_user(email='item1@user.com', password='1234test1')
        followed_profile = Profile.objects.create(
            first_name='test',
            user=followed_user
        )
        response = self.client.get(reverse('home'))
        Follow.objects.create(
            profile_to_follow=followed_profile,
            follower=self.user
        )

        self.assertEqual(0, len(response.context['feed']))


    @factory.django.mute_signals(signals.post_save)
    def test_getHomePageWithArtItemsList_whenNotFollowedAnyProfile__shouldReturnEmptyFeed(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('home'))

        self.assertEqual(0, len(response.context['feed']))