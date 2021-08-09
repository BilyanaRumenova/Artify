from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from artify.accounts.models import Profile
from artify.art_items.models import ArtItem

UserModel = get_user_model()


class ProfileDetailsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(email='bilyana@test.bg', password='test1234')


    def test_getDetails__whenLoggedInUserWithoutArtItems_shouldGetDetailsWithoutArtItems(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('profile details'))

        profile = response.context['profile']
        art_items = list(response.context['art_items'])

        self.assertEqual(response.status_code, 200)
        self.assertListEqual([], art_items)
        self.assertEqual(self.user.id, profile.user_id)

    def test_getDetails__whenLoggedInUserWithArtItems_shouldGetDetailsWithArtItems(self):
        art_item = ArtItem.objects.create(
            type=ArtItem.TYPE_CHOICE_FASHION,
            name='test',
            description='test item description',
            image='path/to/image.png',
            user=self.user,
        )

        self.client.force_login(self.user)

        response = self.client.get(reverse('profile details'))
        profile = response.context['profile']

        self.assertEqual(response.status_code, 200)
        self.assertListEqual([art_item], list(response.context['art_items']))
        self.assertEqual(self.user.id, profile.user_id)

    def test_postDetails__whenLoggedInUserWithImage_shouldChangeProfileImage(self):
        path_to_image = 'path/to/image.png'
        profile = Profile.objects.get(pk=self.user.id)
        profile.profile_image = path_to_image + 'old'
        profile.save()

        self.client.force_login(self.user)

        response = self.client.post(reverse('edit profile details'), data={
            'profile_image': path_to_image,
        })
        self.assertEqual(302, response.status_code)

    def test_postDetails__whenLoggedInUser_shouldChangeNames(self):
        first_name = 'test'
        last_name = 'testov'
        profile = Profile.objects.get(pk=self.user.id)
        profile.first_name = first_name
        profile.last_name = last_name
        profile.save()

        self.client.force_login(self.user)

        response = self.client.post(reverse('edit profile details'), data={
            'first_name': first_name,
            'last_name': last_name,
        })

        self.assertEqual(302, response.status_code)
        self.assertEqual(profile.first_name, 'test')
        self.assertEqual(profile.last_name, 'testov')

    def test_postDetails__whenLoggedInUser_shouldChangeLocation(self):
        location = 'sofia'
        profile = Profile.objects.get(pk=self.user.id)
        profile.location = location
        profile.save()

        self.client.force_login(self.user)

        response = self.client.post(reverse('edit profile details'), data={
            'location': location,
        })

        self.assertEqual(302, response.status_code)
        self.assertEqual(profile.location, 'sofia')









