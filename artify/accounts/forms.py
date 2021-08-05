from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from artify.accounts.models import Profile
from artify.core.forms import BootstrapFormMixin

UserModel = get_user_model()


class SignInForm(BootstrapFormMixin, AuthenticationForm):
    pass


class SignUpForm(BootstrapFormMixin, UserCreationForm):
    # first_name =..... i override save() koito da raboti samo s email pass1 i pass2
    class Meta:
        model = UserModel
        fields = ('email', )


class ProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('items_in_portfolio', 'user',)
