from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('artify.common.urls')),
    # path('art_items/', include('artify.art_items.urls')),
]
