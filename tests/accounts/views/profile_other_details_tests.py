from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from artify.accounts.models import Profile
from artify.art_items.models import ArtItem
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
        art_item = ArtItem.objects.create(
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

    def test_getOtherProfileDetails__whenOtherUserDoesNotExist__shouldRaiseError(self):
        self.client.force_login(self.user)

        self.assertFalse(Profile.objects.filter(
            user_id=5).exists())