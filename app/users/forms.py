from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)

User = get_user_model()


class RegisterForm(UserCreationForm):
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
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "class": "form-control",
                "placeholder": "Email",
            }
        ),
    )
    password1 = forms.CharField(
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
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control",
                "placeholder": "Confirm Password",
            }
        ),
        strip=False,
    )
    field_order = [
        "username",
        "email",
        "password1",
        "password2",
    ]

    class Meta:
        model = User
        fields = [
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
                "checked": True,
                "class": "form-check-input",
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
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "autofocus": True,
                "class": "form-control",
                "placeholder": "Old Password",
            },
        ),
    )
    new_password1 = forms.CharField(
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


class ResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "autofocus": True,
                "class": "form-control",
                "placeholder": "Email",
            },
        ),
    )


class ResetPasswordConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "autofocus": True,
                "class": "form-control",
                "placeholder": "New Password",
            },
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
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
        "new_password1",
        "new_password2",
    ]
