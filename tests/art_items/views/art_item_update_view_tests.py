from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from artify.art_items.forms import ArtItemForm
from tests.base.mixins import ArtItemTestUtils, UserTestUtils
from tests.base.tests import ArtifyTestCase

UserModel = get_user_model()


class UpdateArtItemTest(ArtItemTestUtils, UserTestUtils, ArtifyTestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(
            email='bilyana@test.bg',
            password='test1234'
        )
        self.art_item = self.create_item(
            type='fashion',
            name='test',
            description='test item description',
            image='path/to/image.png',
            user=self.user,
        )

    def test_getUpdateItemWhenSignedInWhenHavePermission(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('edit item', kwargs={
            'pk': self.art_item.id
        }))
        self.assertEqual(200, response.status_code)

    def test_getUpdateItemWhenSignedInWhenDoNotHavePermission__shouldRaiseError(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('edit item', kwargs={
            'pk': self.art_item.id + 1
        }))
        self.assertEqual(404, response.status_code)

    def test_getUpdateItemWithValidDataWhenSignedIn__shouldUpdateArtItem(self):
        self.client.force_login(self.user)
        existing_art_item = self.art_item

        self.client.post(reverse('edit item', kwargs={'pk': existing_art_item.id}), data={
            'type': 'fashion',
            'name': 'new name',
            'description': 'new item description',
            'image': 'path/to/image.png'})

        existing_art_item.refresh_from_db()
        self.assertEqual(existing_art_item.name, 'new name')
        self.assertEqual(self.art_item.description, 'new item description')

        response = self.client.get(reverse('item details', kwargs={'pk': existing_art_item.id}))
        self.assertTemplateUsed(response, 'art_items/item-details.html')


    def test_getUpdateItemWithValidDataWhenSignedIn__shouldSaveForm(self):
        self.client.force_login(self.user)
        existing_art_item = self.art_item

        form_data = {
            'type': 'fashion',
            'name': 'new name',
            'description': 'item description',
            'image': 'path/to/image.png',
        }
        update_item_form = ArtItemForm(
            data=form_data, instance=existing_art_item
        )
        update_item_form.save()
        self.assertEqual(self.art_item.name, 'new name')
        self.assertEqual(self.art_item.type, 'fashion')
        self.assertEqual(self.art_item.description, 'item description')

        response = self.client.get(reverse('item details', kwargs={'pk': existing_art_item.id}))
        self.assertTemplateUsed(response, 'art_items/item-details.html')


    def test_getUpdateItemWithTooShortNameWhenSignedIn__shouldRaiseError(self):
        self.client.force_login(self.user)
        existing_art_item = self.art_item

        form_data = {
            'type': 'fashion',
            'name': '1',
            'description': 'item description',
            'image': 'path/to/image.png',
        }
        update_item_form = ArtItemForm(
            data=form_data, instance=existing_art_item
        )
        with self.assertRaises(ValueError):
            update_item_form.save()
        self.client.get(reverse('item details', kwargs={'pk': existing_art_item.id}))


    def test_getUpdateItemWithValidDataWhenSignedIn__shouldNotUpdateArtItem(self):
        self.client.force_login(self.user)
        existing_art_item = self.art_item

        response = self.client.post(reverse('edit item', kwargs={'pk': existing_art_item.id}), data={
            'type': 'fashion',
            'name': '1',
            'description': 'new item description',
            'image': 'path/to/image.png'})

        existing_art_item.refresh_from_db()
        self.assertEqual(existing_art_item.name, 'test')
        self.assertEqual(self.art_item.description, 'test item description')
        self.assertTemplateUsed(response, 'art_items/item_edit.html')


    def test_getUpdateItemWithTooLongNameWhenSignedIn__shouldRaiseError(self):
        self.client.force_login(self.user)
        existing_art_item = self.art_item

        form_data = {
            'type': 'fashion',
            'name': 'test test test test test test test test test test test ',
            'description': 'item description',
            'image': 'path/to/image.png',
        }
        update_item_form = ArtItemForm(
            data=form_data, instance=existing_art_item
        )
        with self.assertRaises(ValueError):
            update_item_form.save()

    def test_getUpdateItemWithTooLongNameWhenSignedIn__shouldNotUpdateArtItem(self):
        self.client.force_login(self.user)
        existing_art_item = self.art_item

        self.client.post(reverse('edit item', kwargs={'pk': existing_art_item.id}), data={
            'type': 'fashion',
            'name': 'test test test test test test test test test test test ',
            'description': 'new item description',
            'image': 'path/to/image.png'})

        existing_art_item.refresh_from_db()
        self.assertEqual(existing_art_item.name, 'test')
        self.assertEqual(self.art_item.description, 'test item description')
        response = self.client.get(reverse('item details', kwargs={'pk': existing_art_item.id}))
        self.assertTemplateUsed(response, 'art_items/item-details.html')

    def test_getUpdateItemWithTooLongDescriptionWhenSignedIn__shouldRaiseError(self):
        self.client.force_login(self.user)
        existing_art_item = self.art_item

        form_data = {
            'type': 'fashion',
            'name': 'test',
            'description': 'item description item description item description item description item description '
                           'item description item description item description item description item description ',
            'image': 'path/to/image.png',
        }
        update_item_form = ArtItemForm(
            data=form_data, instance=existing_art_item
        )
        with self.assertRaises(ValueError):
            update_item_form.save()

    def test_getUpdateItemWithTooLongDescriptionWhenSignedIn__shouldNotUpdateArtItem(self):
        self.client.force_login(self.user)
        existing_art_item = self.art_item

        response = self.client.post(reverse('edit item', kwargs={'pk': existing_art_item.id}), data={
            'type': 'fashion',
            'name': 'test',
            'description': 'item description item description item description item description item description '
                           'item description item description item description item description item description ',
            'image': 'path/to/image.png'})

        existing_art_item.refresh_from_db()
        self.assertEqual(existing_art_item.name, 'test')
        self.assertEqual(self.art_item.description, 'test item description')

        self.assertTemplateUsed(response, 'art_items/item_edit.html')



