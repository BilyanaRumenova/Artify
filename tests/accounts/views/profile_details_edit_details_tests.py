from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse

from artify.accounts.forms import ProfileForm
from artify.accounts.models import Profile

UserModel = get_user_model()


class EditProfileDetailsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(email='bilyana@test.bg', password='test1234')

    def test_getDetails__whenLoggedInUserWithImage_shouldGetProfileImage(self):
        path_to_image = 'path/to/image.png'
        profile = Profile.objects.get(pk=self.user.id)
        profile.profile_image = path_to_image

        self.client.force_login(self.user)

        response = self.client.get(reverse('edit profile details'), data={
            'profile_image': path_to_image,
        })
        self.assertEqual(200, response.status_code)
        self.assertEqual(profile.profile_image, 'path/to/image.png')

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
        self.assertEqual(profile.profile_image, 'path/to/image.pngold')


    def test_getDetails__whenLoggedInUser_shouldGetNames(self):
        first_name = 'test'
        last_name = 'testov'
        profile = Profile.objects.get(pk=self.user.id)
        profile.first_name = first_name
        profile.last_name = last_name

        self.client.force_login(self.user)

        response = self.client.get(reverse('edit profile details'), data={
            'first_name': first_name,
            'last_name': last_name,
        })

        self.assertEqual(200, response.status_code)
        self.assertEqual(profile.first_name, 'test')
        self.assertEqual(profile.last_name, 'testov')

    def test_postValidDetails__whenLoggedInUser_shouldChangeNames(self):
        first_name = 'test'
        last_name = 'testov'
        profile = Profile.objects.get(pk=self.user.id)
        profile.first_name = first_name + 'new'
        profile.last_name = last_name + 'new'
        profile.save()

        self.client.force_login(self.user)

        response = self.client.post(reverse('edit profile details'), data={
            'first_name': profile.first_name,
            'last_name': profile.last_name,
        })

        self.assertEqual(302, response.status_code)
        self.assertEqual(profile.first_name, 'testnew')
        self.assertEqual(profile.last_name, 'testovnew')

    def test_postInvalidFirstName__whenLoggedInUser_shouldNotChangeFirstName(self):
        profile = Profile.objects.get(pk=self.user.id)
        profile.first_name = 'test'

        self.client.force_login(self.user)
        form_data = {
            'first_name': profile.first_name + 'something something something something something something'                                    
                          'something something something something something something something something'
                          'something something something something something something something something',
        }
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(profile.first_name, 'test')

    def test_postInvalidLastName__whenLoggedInUser_shouldNotChangeLastName(self):
        profile = Profile.objects.get(pk=self.user.id)
        profile.last_name = 'testov'

        self.client.force_login(self.user)
        form_data = {
            'last_name': profile.last_name + 'something something something something something something'                                    
                          'something something something something something something something something'''
        }
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(profile.last_name, 'testov')


    def test_getDetails__whenLoggedInUser_shouldGetLocation(self):
        location = 'sofia'
        profile = Profile.objects.get(pk=self.user.id)
        profile.location = location

        self.client.force_login(self.user)

        response = self.client.post(reverse('edit profile details'), data={
            'location': profile.location,
        })

        self.assertEqual(200, response.status_code)
        self.assertEqual(profile.location, 'sofia')

    def test_postDetails__whenLoggedInUser_shouldChangeLocation(self):
        location = 'sofia'
        profile = Profile.objects.get(pk=self.user.id)
        profile.location = location + 'bg'
        profile.save()

        self.client.force_login(self.user)

        response = self.client.post(reverse('edit profile details'), data={
            'location': profile.location,
        })

        self.assertEqual(302, response.status_code)
        self.assertEqual(profile.location, 'sofiabg')

    def test_postInvalidLocation__whenLoggedInUser_shouldNotChangeLocation(self):
        profile = Profile.objects.get(pk=self.user.id)

        self.client.force_login(self.user)
        form_data = {
            'location': 'bg444444444444444444444444444444333333333333333333333333',
        }
        form = ProfileForm(data=form_data)
        response = self.client.post(reverse('edit profile details'), data=form_data)
        if form.is_valid():
            profile.location = form_data['location']
        self.assertEqual(200, response.status_code)
        self.assertFalse(profile.location, 'bg444444444444444444444444444444333333333333333333333333')
        self.assertEqual(profile.location, '')

    def test_postValidLocation__whenLoggedInUser_shouldChangeLocation(self):
        profile = Profile.objects.get(pk=self.user.id)

        self.client.force_login(self.user)
        form_data = {
            'location': 'bg',
        }
        form = ProfileForm(data=form_data)
        response = self.client.post(reverse('edit profile details'), data=form_data)
        if form.is_valid():
            profile.location = form_data['location']

        self.assertEqual(302, response.status_code)
        self.assertEqual(profile.location, 'bg')




