from django.urls import path
from artify.common.views import LandingPageView

urlpatterns = (
    path('', LandingPageView.as_view(), name='index'),
)