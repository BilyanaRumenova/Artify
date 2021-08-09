from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView

from artify.accounts.forms import SignUpForm, SignInForm, ProfileForm
from artify.accounts.models import Profile, Follow, ArtifyUser
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


class SignOutView(LoginRequiredMixin, LogoutView):
    next_page = 'index'
    template_name = None

    def get_success_url(self):
        logout(self.request)
        return reverse('index')


class ProfileDetailsView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/user_profile.html'
    model = Profile
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_items = ArtItem.objects.filter(user_id=self.request.user.id)

        context['profile'] = self.object
        context['art_items'] = user_items

        return context


class EditProfileDetailsView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/edit_profile.html'
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy('edit profile details')
    object = None

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get(self, request, *args, **kwargs):
        self.object = Profile.objects.get(pk=request.user.id)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = Profile.objects.get(pk=request.user.id)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.profile_image = form.cleaned_data['profile_image']
        self.object.location = form.cleaned_data['location']
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_items = ArtItem.objects.filter(user_id=self.request.user.id)

        context['profile'] = self.object
        context['art_items'] = user_items

        return context

    def get_success_url(self):
        url = reverse_lazy('profile details')
        return url


class FollowProfileView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        profile_to_follow = Profile.objects.get(pk=self.kwargs['pk'])
        follow_object_by_user = profile_to_follow.follow_set.filter(follower_id=request.user).first()

        if follow_object_by_user:
            follow_object_by_user.delete()
        else:
            follow = Follow(
                profile_to_follow=profile_to_follow,
                follower=request.user,
            )
            follow.save()
        return redirect('other profile details', profile_to_follow.user_id)


class OtherProfileDetailsView(View):
    pass


@login_required
def other_profile_details(request, pk):
    other_profile = Profile.objects.get(pk=pk)
    other_profile_items = ArtItem.objects.filter(user_id=other_profile.user_id)
    is_owner = other_profile.user == request.user
    if is_owner:
        return redirect('profile details')
    context = {
        'profile': other_profile,
        'art_items': other_profile_items,
        'is_owner': is_owner,
    }
    return render(request, 'accounts/other profile.html', context)


