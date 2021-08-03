from django.urls import path

from artify.accounts.views import SignUpView, SignInView, SignOutView, ProfileDetailsView

urlpatterns = (
    path('signin/', SignInView.as_view(), name='sign in user'),
    path('signup/', SignUpView.as_view(), name='sign up user'),
    path('signout/', SignOutView.as_view(), name='sign out user'),
    path('profile/', ProfileDetailsView.as_view(), name='profile details'),
    path('profile/<int:pk>', ProfileDetailsView.as_view(), name='profile details'),
    # path('signin/', sign_in_user, name='sign in user'),
    # path('signup/', sign_up_user, name='sign up user'),
    # path('signout/', sign_out_user, name='sign out user'),
    # path('profile/', profile_details, name='profile details'),
)
