from django.contrib.auth import get_user_model
from django.test import Client

from artify.art_items.models import ArtItem, Comment
from tests.base.mixins import ArtItemTestUtils, UserTestUtils
from tests.base.tests import ArtifyTestCase

UserModel = get_user_model()


class CommentViewTest(ArtItemTestUtils, UserTestUtils, ArtifyTestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(email='bilyana@test.bg', password='test1234')

    def test_PostCommentWhenSignedInWithValidData__shouldPostComment(self):
        self.client.force_login(self.user)
        item_user = self.create_user(email='item@user.com', password='12345qwe')
        art_item = self.create_item(
            type=ArtItem.TYPE_CHOICE_PORTRAIT,
            name='Test Art Item',
            description='Test item description',
            image='path/to/image.png',
            user=item_user,
        )
        Comment.objects.create(comment='test',
                               item=art_item,
                               user=self.user
                               )
        self.assertTrue(Comment.objects.filter(comment='test').exists())
        self.assertFalse(Comment.objects.filter(comment='test3').exists())


