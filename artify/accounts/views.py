from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DetailView, FormView

from artify.accounts.forms import SignUpForm, SignInForm, ProfileForm
from artify.accounts.models import Profile, Follow
from artify.art_items.models import ArtItem

UserModel = get_user_model()


class SignUpView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid


class SignInView(LoginView):
    template_name = 'accounts/signin.html'
    authentication_form = SignInForm

    def get_success_url(self):
        return reverse('index')


class SignOutView(LogoutView):
    next_page = 'index'
    template_name = None

    def get_success_url(self):
        logout(self.request)
        return reverse('index')


class ProfileDetailsView(LoginRequiredMixin, FormView):
    template_name = 'accounts/user_profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('profile details')

    def form_valid(self, form):
        profile = Profile.objects.get(pk=self.request.user.id)
        profile.profile_image = form.cleaned_data['profile_image']
        profile.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = Profile.objects.get(pk=self.request.user.id)
        user_items = ArtItem.objects.filter(user_id=self.request.user.id)

        context['profile'] = profile
        context['art_items'] = user_items

        return context


class OtherProfileDetailsView(FormView):
    template_name = 'accounts/other profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('other profile details')

    def form_valid(self, form):
        profile = Profile.objects.get()
        profile.profile_image = form.cleaned_data['profile_image']
        profile.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = Profile.objects.get(pk=self.request.user.id)
        user_items = ArtItem.objects.filter(user_id=self.request.user.id)

        context['profile'] = profile
        context['art_items'] = user_items

        return context

# class OtherProfileDetailsView(DetailView):
#     model = Profile
#     template_name = 'accounts/other profile.html'
#     context_object_name = 'profile'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         profile = self.get_object()
#
#         context['is_followed'] = profile.follow_set.filter(follower=self.request.user.id).exists()
#         context['is_owner'] = profile.user == self.request.user
#
#         # user_items = Portfolio.objects.filter(user_id=profile.user)
#         # context['art_items'] = user_items
#
#         return context


class FollowProfileView(View):
    def get(self, request, **kwargs):
        profile_to_follow = Profile.objects.get(pk=self.kwargs['pk'])
        follow_object_by_user = profile_to_follow.follow_set.filter(follower_id=request.user).first()

        if follow_object_by_user:
            follow_object_by_user.delete()
        else:
            follow = Follow(
                user_to_follow=profile_to_follow,
                follower=request.user,
            )
            follow.save()
        return redirect('other profile details', profile_to_follow.user_id)

