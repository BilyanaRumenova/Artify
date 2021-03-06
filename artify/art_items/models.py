from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models

from artify.accounts.models import ArtifyUser, Profile

from cloudinary import models as cloudinary_models


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
    image =cloudinary_models.CloudinaryField(
        resource_type='image',
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.name}'


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
        validators=[MinLengthValidator(2),
                    MaxLengthValidator(50)],
    )
    item = models.ForeignKey(
        ArtItem,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.comment}'


class Follow(models.Model):
    profile_to_follow = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )
    follower = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )
