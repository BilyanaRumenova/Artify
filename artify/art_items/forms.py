from django import forms

from artify.art_items.models import ArtItem, Comment
from artify.core.forms import BootstrapFormMixin


class ArtItemForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ArtItem
        fields = '__all__'


class EditArtItemForm(ArtItemForm):
    class Meta:
        model = ArtItem
        fields = '__all__'
        widgets = {
            'type': forms.TextInput(
                attrs={
                    'readonly': 'readonly'
                }
            )
        }


class CommentForm(forms.ModelForm):
    item_pk = forms.IntegerField(
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Comment
        fields = ('comment', 'item_pk')

    def save(self, commit=True):
        item_pk = self.cleaned_data['item_pk']
        item = ArtItem.objects.get(pk=item_pk)
        comment = Comment(
            comment=self.cleaned_data['comment'],
            item=item,
        )
        if commit:
            comment.save()

        return comment
