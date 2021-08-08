from django.contrib.auth import get_user_model
from django.urls import reverse

from artify.accounts.models import Follow, Profile
from tests.base.mixins import ArtItemTestUtils, UserTestUtils
from tests.base.tests import ArtifyTestCase

UserModel = get_user_model()


class FollowProfileViewTests(ArtItemTestUtils, UserTestUtils, ArtifyTestCase):

    def test_followProfile__whenProfileNotFollowedYet__shouldCreateFollow(self):
        self.client.force_login(self.user)
        user_to_follow = self.create_user(email='item@user.bg', password='1234test')

        response = self.client.get(reverse('follow profile', kwargs={'pk': user_to_follow.id}))

        self.assertEqual(302, response.status_code)

        follow_exists = Follow.objects.filter(
            profile_to_follow_id=user_to_follow.id,
            follower_id=self.user.id
        ).exists()
        self.assertTrue(follow_exists)

    # def test_followProfile__whenProfileAlreadyFollowed__shouldDeleteFollow(self):
    #     self.client.force_login(self.user)
    #     user_to_follow = self.create_user(email='item@user.bg', password='1234test')
    #     profile_to_follow = self.create_profile_with_follow(
    #         follower=self.user,
    #
    #     )
    #     response = self.client.get(reverse('follow profile', kwargs={'pk': profile_to_follow.pk}))
    #     self.assertEqual(302, response.status_code)
    #
    #     follow_exists = Follow.objects.filter(
    #         profile_to_follow_id=profile_to_follow.pk,
    #         follower_id=self.user.id
    #     ).exists()
    #     self.assertFalse(follow_exists)
    #
    #
    #

