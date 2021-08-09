from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from artify.art_items.forms import ArtItemForm
from tests.base.mixins import ArtItemTestUtils, UserTestUtils
from tests.base.tests import ArtifyTestCase

UserModel = get_user_model()


class ArtItemFormTest(ArtItemTestUtils, UserTestUtils, ArtifyTestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(email='bilyana@test.bg', password='test1234')

    def test_art_item_empty_form(self):
        form = ArtItemForm()
        self.assertIn('type', form.fields)
        self.assertIn('name', form.fields)
        self.assertIn('description', form.fields)
        self.assertIn('image', form.fields)
        self.assertNotIn('user', form.fields)

    def test_artItemFormWithValidData__shouldReturnTrue(self):
        self.client.force_login(self.user)
        form_data = {
            'type': 'portrait',
            'name': 'Test Art Item',
            'description': 'Test item description',
            'image': 'path/to/image.png',
        }
        form = ArtItemForm(data=form_data)
        self.assertTrue(form.is_valid())






