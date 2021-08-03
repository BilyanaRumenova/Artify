from django.contrib.auth import login, logout, get_user_model, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse

from django.views.generic import CreateView, UpdateView

from artify.accounts.forms import SignUpForm, SignInForm, ProfileForm
from artify.accounts.models import Profile
from artify.art_items.models import ArtItem
from artify.core.forms import BootstrapFormMixin

UserModel = get_user_model()


class SignUpView(CreateView):
    template_name = 'accounts/signup.html'
    model = UserModel
    form_class = SignUpForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        valid = super(SignUpView, self).form_valid(form)
        email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
        new_user = authenticate(email=email, password=password)
        login(self.request, new_user)
        return valid


class SignInView(LoginView):
    template_name = 'accounts/signin.html'
    form_class = SignInForm

    def get_success_url(self):
        return reverse('index')


class SignOutView(LogoutView):
    next_page = 'index'
    template_name = None

    def get_success_url(self):
        logout(self.request)
        return reverse('index')


class ProfileDetailsView(UpdateView):
    template_name = 'accounts/user_profile.html'
    form_class = ProfileForm
    model = Profile
    success_url = reverse_lazy('profile details')

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk', None)
        user = self.request.user if pk is None else UserModel.objects.get(pk=pk)
        return user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['profile'] = self.get_object().user

        user_items = ArtItem.objects.filter(user_id=self.request.user.id)
        context['art_items'] = user_items

        return context


# def sign_up_user(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('index')
#     else:
#         form = SignUpForm()
#
#     context = {
#         'form': form,
#     }
#     return render(request, 'accounts/signup.html', context)

# def sign_in_user(request):
#     if request.method == 'POST':
#         form = SignInForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('index')
#     else:
#         form = SignInForm()
#
#     context = {
#         'form': form,
#     }
#     return render(request, 'accounts/signin.html', context)



# @login_required
# def sign_out_user(request):
#     logout(request)
#     return redirect('index')


# @login_required
# def profile_details(request):
#     profile = Profile.objects.get(pk=request.user.id)
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('profile details')
#     else:
#         form = ProfileForm(instance=profile)
#
#     user_items = ArtItem.objects.filter(user_id=request.user.id)
#
#
#     context = {
#         'form': form,
#         'art_items': user_items,
#         'profile': profile,
#     }
#     return render(request, 'accounts/user_profile.html', context)
