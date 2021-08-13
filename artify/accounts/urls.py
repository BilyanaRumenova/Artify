from django.urls import path

from artify.accounts.views import SignUpView, SignInView, SignOutView, ProfileDetailsView, \
    FollowProfileView, other_profile_details, EditProfileDetailsView

urlpatterns = (
    path('signin/', SignInView.as_view(), name='sign in user'),
    path('signup/', SignUpView.as_view(), name='sign up user'),
    path('signout/', SignOutView.as_view(), name='sign out user'),
    path('profile/', ProfileDetailsView.as_view(), name='profile details'),
    path('edit/', EditProfileDetailsView.as_view(), name='edit profile details'),
    # path('profile/<int:pk>', OtherProfileDetailsView.as_view(), name='other profile details'),
    path('profile/<int:pk>', other_profile_details, name='other profile details'),
    path('follow/<int:pk>', FollowProfileView.as_view(), name='follow profile'),

)
