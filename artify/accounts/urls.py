from django.urls import path

from artify.accounts.views import sign_in_user, sign_up_user, sign_out_user, profile_details

urlpatterns = (
    path('signin/', sign_in_user, name='sign in user'),
    path('signup/', sign_up_user, name='sign up user'),
    path('signout/', sign_out_user, name='sign out user'),
    path('profile/', profile_details, name='profile details'),
)