from django.urls import path

from artify.common.views import landing_page

urlpatterns = (
    path('', landing_page, name='landing page'),
)