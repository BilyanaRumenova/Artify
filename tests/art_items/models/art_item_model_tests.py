from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase, Client

from artify.art_items.models import ArtItem

UserModel = get_user_model()


class ArtItemModelTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(email='bilyana@test.bg', password='test1234')

    def create_art_item_with_proper_attrs(self):
        self.client.force_login(self.user)
        return ArtItem.objects.create(type=ArtItem.TYPE_CHOICE_PORTRAIT, name='test', description='description test',
                                      image='path/to/image.png',
                                      user=self.user)

    def test_artItemCreationIsValid__shouldCreateArtItem(self):
        item = self.create_art_item_with_proper_attrs()
        self.assertTrue(isinstance(item, ArtItem))

    def test_artItemNameIsTooLongCreationIsInvalid__shouldNotCreateArtItem(self):
        item = ArtItem(type=ArtItem.TYPE_CHOICE_PORTRAIT,
                       name='testtesttesttesttesttesttesttesttesttesttesttesttest',
                       description='description test',
                       image='path/to/image.png',
                       user=self.user
                       )
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_artItemNameIsTooShortCreationIsInvalid__shouldNotCreateArtItem(self):
        item = ArtItem(type=ArtItem.TYPE_CHOICE_PORTRAIT,
                       name='t',
                       description='description test',
                       image='path/to/image.png',
                       user=self.user
                       )
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_artItemDescriptionIsTooLongCreationIsInvalid__shouldNotCreateArtItem(self):
        item = ArtItem(type=ArtItem.TYPE_CHOICE_PORTRAIT,
                       name='test name',
                       description='testtesttesttesttesttesttesttesttesttesttesttesttest'
                                   'testtesttesttesttesttesttesttesttesttesttesttesttest'
                                   'testtesttesttesttesttesttesttesttesttesttesttesttest'
                                   'testtesttesttesttesttesttesttesttesttesttesttesttest',
                       image='path/to/image.png',
                       user=self.user
                       )
        with self.assertRaises(ValidationError):
            item.full_clean()
