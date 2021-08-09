from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase, Client

from artify.art_items.models import ArtItem, Comment

UserModel = get_user_model()


class CommentModelTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(email='bilyana@test.bg', password='test1234')
        item = ArtItem.objects.create(type=ArtItem.TYPE_CHOICE_PORTRAIT, name='test', description='description test',
                                      image='path/to/image.png',
                                      user=self.user)
        self.comment = Comment.objects.create(comment='test comment', item=item, user=self.user)

    def test_CommentIsValidCreationIsSuccessful__shouldCreateComment(self):
        self.assertTrue(self.comment)

    def test_CommentIsTooLongInvalidCreationIsUnsuccessful__shouldNotCreateComment(self):
        comment = Comment(comment='test comment test comment test comment test comment test comment'
                                  'test comment test comment test comment test comment test comment '
                                  'test comment test', )
        self.assertRaises(ValidationError, comment.full_clean)

    def test_CommentIsTooShortInvalidCreationIsUnsuccessful__shouldNotCreateComment(self):
        comment = Comment(comment='t')
        self.assertRaises(ValidationError, comment.full_clean)



