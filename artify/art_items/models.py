from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

import artify.accounts.models
from artify.accounts.models import ArtifyUser, Profile


UserModel = get_user_model()


class ArtItem(models.Model):
    TYPE_CHOICE_PHOTOGRAPHY = 'photography'
    TYPE_CHOICE_PAINTING = 'painting'
    TYPE_CHOICE_PORTRAIT = 'portrait'
    TYPE_CHOICE_FASHION = 'fashion'

    TYPE_CHOICES = (
        (TYPE_CHOICE_PHOTOGRAPHY, 'Photography'),
        (TYPE_CHOICE_PAINTING, 'Painting'),
        (TYPE_CHOICE_PORTRAIT, 'Portrait'),
        (TYPE_CHOICE_FASHION, 'Fashion'),
    )

    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
    )
    name = models.CharField(
        validators=[MinLengthValidator(2)],
        max_length=25,
    )

    description = models.TextField(
        max_length=100,
    )

    image = models.ImageField(
        upload_to='arts',
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )


class Like(models.Model):
    item = models.ForeignKey(
        ArtItem,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )


class Comment(models.Model):
    comment = models.TextField(
        validators=[MinLengthValidator(2)],
        max_length=50,
    )
    item = models.ForeignKey(
        ArtItem,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )


class Collection(models.Model):
   owner = models.OneToOneField(
       UserModel,
       # artify.accounts.models.Profile,
       on_delete=models.CASCADE,
       related_name="author",
   )
   content = models.ForeignKey(
       ArtItem,
       on_delete=models.CASCADE,
   )