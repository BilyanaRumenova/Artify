import os
from os.path import join

from django import forms
from django.conf import settings

from artify.art_items.models import ArtItem, Comment
from artify.core.forms import BootstrapFormMixin


class ArtItemForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ArtItem
        exclude = ('user',)


class EditArtItemForm(ArtItemForm):

    def save(self, commit=True):
        db_item = ArtItem.objects.get(pk=self.instance.id)
        if commit:
            image_path = join(settings.MEDIA_ROOT, str(db_item.image))
            os.remove(image_path)
        return super().save(commit)

    class Meta:
        model = ArtItem
        exclude = ('user',)
        widgets = {
            'type': forms.TextInput(
                attrs={
                    'readonly': 'readonly'
                }
            ),
        }


class CommentForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('comment', )


