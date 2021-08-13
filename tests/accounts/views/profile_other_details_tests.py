import factory
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from artify.accounts import signals
from artify.accounts.models import Profile
from artify.art_items.models import ArtItem, Follow
from tests.base.mixins import ArtItemTestUtils, UserTestUtils
from tests.base.tests import ArtifyTestCase

UserModel = get_user_model()


class OtherProfileDetailsTest(ArtItemTestUtils, UserTestUtils, ArtifyTestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(email='bilyana@test.bg', password='test1234')

    def test_getOtherProfileDetails__whenOtherUserIsWithoutArtItems__shouldGetDetailsWithoutArtItems(self):
        self.client.force_login(self.user)

        other_user = self.create_user(email='other@user.bg', password='1234test')
        response = self.client.get(reverse('other profile details', kwargs={'pk': other_user.id}))

        other_profile = response.context['profile']
        other_profile_art_items = list(response.context['art_items'])

        self.assertEqual(200, response.status_code)
        self.assertNotEqual(self.user.id, other_profile.user_id)
        self.assertListEqual([], other_profile_art_items)


    def test_getOtherProfileDetails__whenOtherUserHasArtItems__shouldGetDetailsWithArtItems(self):
        self.client.force_login(self.user)

        other_user = self.create_user(email='other@user.bg', password='1234test')
        art_item = self.create_item(
            type=ArtItem.TYPE_CHOICE_FASHION,
            name='test',
            description='test item description',
            image='path/to/image.png',
            user=other_user,
        )
        response = self.client.get(reverse('other profile details', kwargs={'pk': other_user.id}))

        other_profile = response.context['profile']
        other_profile_art_items = list(response.context['art_items'])
        other_profile_is_owner = response.context['is_owner']

        self.assertEqual(200, response.status_code)
        self.assertNotEqual(self.user.id, other_profile.user_id)
        self.assertListEqual([art_item], other_profile_art_items)
        self.assertFalse(other_profile_is_owner)

    @factory.django.mute_signals(signals.post_save)
    def test_getOtherProfileDetails__whenOtherProfileHasFollowers__shouldGetDetailsWithFollowers(self):
        self.client.force_login(self.user)

        other_user = self.create_user(email='other@user.bg', password='1234test')
        other_profile = self.create_profile(user=other_user)

        Follow.objects.create(
            profile_to_follow=other_profile,
            follower=self.user
        )

        response = self.client.get(reverse('other profile details', kwargs={'pk': other_user.id}))

        other_profile_is_followed = response.context['is_followed']
        other_profile_is_owner = response.context['is_owner']

        self.assertEqual(200, response.status_code)
        self.assertTrue(other_profile_is_followed)
        self.assertFalse(other_profile_is_owner)

    @factory.django.mute_signals(signals.post_save)
    def test_getOtherProfileDetails__whenOtherProfileHasNoFollowers__shouldGetDetailsWithoutFollowers(self):
        self.client.force_login(self.user)

        other_user = self.create_user(email='other@user.bg', password='1234test')
        self.create_profile(user=other_user)

        response = self.client.get(reverse('other profile details', kwargs={'pk': other_user.id}))

        other_profile_is_followed = response.context['is_followed']

        self.assertEqual(200, response.status_code)
        self.assertFalse(other_profile_is_followed)

    def test_getOtherProfileDetails__whenOtherUserDoesNotExist__shouldRaiseError(self):
        self.client.force_login(self.user)
        self.assertFalse(Profile.objects.filter(
            user_id=5).exists())





