# from django.contrib.auth import get_user_model
# from django.db import models
#
# UserModel = get_user_model()
#
#
# class ArtItem(models.Model):
#     TYPE_CHOICE_PHOTOGRAPHY = 'photography'
#     TYPE_CHOICE_PAINTING = 'painting'
#     TYPE_CHOICE_PORTRAIT = 'portrait'
#     TYPE_CHOICE_FASHION = 'fashion'
#
#     TYPE_CHOICES = (
#         (TYPE_CHOICE_PHOTOGRAPHY, 'Photography'),
#         (TYPE_CHOICE_PAINTING, 'Painting'),
#         (TYPE_CHOICE_PORTRAIT, 'Portrait'),
#         (TYPE_CHOICE_FASHION, 'Fashion'),
#     )
#
#     type = models.CharField(
#         max_length=20,
#         choices=TYPE_CHOICES,
#     )
#     name = models.CharField(
#         max_length=25,
#     )
#
#     description = models.TextField()
#     image = models.ImageField(
#         upload_to='pets',
#     )
#
#     user = models.ForeignKey(
#         UserModel,
#         on_delete=models.CASCADE,
#     )
#
# class Like(models.Model):
#     art_item = models.ForeignKey(
#         ArtItem,
#         on_delete=models.CASCADE,
#     )
#     user = models.ForeignKey(
#         UserModel,
#         on_delete=models.CASCADE,
#     )