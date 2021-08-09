from django.test import TestCase

from artify.accounts.forms import ProfileForm


class ProfileFormTest(TestCase):
    def test_profileFormWithValidData__shouldReturnTrue(self):
        form_data = {
            'first_name': 'something',
            'last_name': 'something',
            'profile_image': 'path/to/img.png',
            'location': 'somewhere',
        }
        form = ProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_profileFormWithInvalidFirstName__shouldReturnFalse(self):
        form_data = {
            'first_name': 'something something something something something something something something'
                          'something something something something something something something something'
                          'something something something something something something something something',
            'last_name': 'something',
            'profile_image': 'path/to/img.png',
            'location': 'somewhere',
        }
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_profileFormWithInvalidLastName__shouldReturnFalse(self):
        form_data = {
            'first_name': '',
            'last_name': 'something something something something something something something something'
                          'something something something something something something something something'
                          'something something something something something something something something',
            'profile_image': 'path/to/img.png',
            'location': 'somewhere',
        }
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_profileFormWithInvalidLocation__shouldReturnFalse(self):
        form_data = {
            'first_name': 'something',
            'last_name': 'something',
            'profile_image': 'path/to/img.png',
            'location': 'somewhere somewhere somewhere somewhere somewhere somewhere somewhere somewhere',
        }
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

