from django.contrib.auth import get_user_model

from artify.accounts.models import Profile
from artify.art_items.models import ArtItem, Like, Follow

UserModel = get_user_model()


class ArtItemTestUtils:
    def create_item(self, **kwargs):
        return ArtItem.objects.create(**kwargs)

    def create_item_with_like(self, like_user, **kwargs):
        art_item = self.create_item(**kwargs)
        Like.objects.create(
            item=art_item,
            user=like_user,
        )
        return art_item


class UserTestUtils:
    def create_user(self, **kwargs):
        return UserModel.objects.create(**kwargs)

    def create_profile(self, **kwargs):
        return Profile.objects.create(**kwargs)

    def create_profile_with_follow(self, follower, **kwargs):
        profile_to_follow = self.create_profile(**kwargs)
        Follow.objects.create(
            profile_to_follow=profile_to_follow,
            follower=follower
        )
        return profile_to_follow

