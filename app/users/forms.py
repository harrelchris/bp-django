from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    UserCreationForm,
)

User = get_user_model()


class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )


class LoginForm(AuthenticationForm):
    remember = forms.BooleanField(required=False)


class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "email",
        ]


class ChangePasswordForm(PasswordChangeForm):
    pass
