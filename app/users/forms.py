from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    UserCreationForm,
)

User = get_user_model()


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        help_text="A unique name",
        label="Username",
        widget=forms.TextInput(
            attrs={
                "autocomplete": "username",
                "autofocus": True,
                "class": "form-control",
                "placeholder": "Username",
            },
        ),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email-address",
                "class": "form-control",
                "placeholder": "Email",
            }
        ),
        help_text="Your email address",
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control",
                "placeholder": "Password",
            }
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control",
                "placeholder": "Confirm Password",
            }
        ),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )
    field_order = [
        "username",
        "email",
        "password1",
        "password2",
    ]


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "autocomplete": "username",
                "autofocus": True,
                "class": "form-control",
                "placeholder": "Username",
            },
        ),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "password",
                "class": "form-control",
                "placeholder": "Password",
            },
        ),
    )
    remember = forms.BooleanField(
        label="Remember Me",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "autocomplete": "remember-me",
                "checked": True,
                "class": "form-check-input",
                "placeholder": "Remember Me",
            },
        ),
    )


class EmailChangeForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "autofocus": True,
                "class": "form-control",
                "placeholder": "Email",
            },
        ),
    )

    class Meta:
        model = User
        fields = [
            "email",
        ]


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "old-password",
                "autofocus": True,
                "class": "form-control",
                "placeholder": "Old Password",
            },
        ),
    )
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control",
                "placeholder": "New Password",
            },
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control",
                "placeholder": "Confirm New Password",
            },
        ),
    )
    field_order = [
        "old_password",
        "new_password1",
        "new_password2",
    ]
