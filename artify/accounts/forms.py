from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from artify.accounts.models import Profile
from artify.core.forms import BootstrapFormMixin

UserModel = get_user_model()


class SignInForm(BootstrapFormMixin, forms.Form):
    user = None
    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput(),
    )

    error_messages = {
        'invalid_login': (
            "Please enter a correct %(email)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': ("This account is inactive."),
    }

    def clean(self):
        self.user = authenticate(
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
        )
        if not self.user:
            raise ValidationError('Email and/or password incorrect')

    def save(self):
        return self.user


class SignUpForm(BootstrapFormMixin, UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email', )


class ProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('profile_image', )
