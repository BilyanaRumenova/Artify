from django.contrib import admin

from artify.art_items.models import ArtItem


@admin.register(ArtItem)
class ArtifyItemAdmin(admin.ModelAdmin):
    list_display = ('type', 'name', 'description', 'image', 'likes_count',)
    list_filter = ('type',)

    def likes_count(self, obj):
        return obj.like_set.count()



# admin.site.register(ArtItem, ArtItemAdmin)
