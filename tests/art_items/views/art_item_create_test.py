from django.urls import reverse

from tests.base.mixins import ArtItemTestUtils, UserTestUtils
from tests.base.tests import ArtifyTestCase


class CreateNewArtItemTest(ArtItemTestUtils, UserTestUtils, ArtifyTestCase):
    def setUp(self):
        item_user_1 = self.create_user(email='item1@user.com', password='1234test1')
        self.form_data = {
            'type': 'photography',
            'name': 'test name',
            'description': 'test description',
            'image': 'image.png',
            'user': item_user_1,
        }

    def test_createItemWhenNotSignedIn__shouldRaiseError(self):
        response = self.client.get(reverse('create item'), follow=True)
        self.assertEqual(404, response.status_code)

    def test_new_item_form_is_valid(self):
        self.client.login()
        response = self.client.get(reverse('create item'))
        self.assertEqual(302, response.status_code)

        item = self.create_item(
            type='photography',
            name='test item',
            description='test description',
            image='path/to/image.png',
        )
        if item.objects.full_clean():
            item.save()
            self.assertEqual(response.status_code, 200)
            # self.assertTrue(item)