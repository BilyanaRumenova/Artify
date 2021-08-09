from unittest import TestCase

from artify.art_items.forms import CommentForm


class CommentTestForm(TestCase):

    def test_commentFormWhenCommentValid__shouldPostComment(self):
        form_data = {
            'comment': 'test comment',
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_commentFormCommentFormTooShort__shouldNotPostComment(self):
        form_data = {
            'comment': 't',
        }
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_commentFormWhenCommentTooLong__shouldNotPostComment(self):
        form_data = {
            'comment': 'testtesttesttesttesttesttesttesttesttesttesttesttesttest',
        }
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
