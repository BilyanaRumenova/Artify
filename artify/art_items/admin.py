from django.contrib import admin

from artify.art_items.models import ArtItem, Comment, Like, Follow


@admin.register(ArtItem)
class ArtifyItemAdmin(admin.ModelAdmin):
    list_display = ('type', 'name', 'description', 'image', 'likes_count',)
    list_filter = ('type',)

    def likes_count(self, obj):
        return obj.like_set.count()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'comment',)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'profile_to_follow',)