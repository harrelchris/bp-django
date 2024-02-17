from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout, update_session_auth_hash
from django.core.mail import send_mail
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse_lazy

from . import forms, models

User = get_user_model()


def register_user(request: HttpRequest, form: forms.RegisterForm) -> User:
    user = form.save()
    login(request=request, user=user)
    send_verification_email(request=request)
    return user


def login_user(request: HttpRequest, form: forms.LoginForm) -> User:
    user = authenticate(
        request=request,
        username=form.cleaned_data["username"],
        password=form.cleaned_data["password"],
    )
    if user:
        if not form.cleaned_data.get("remember", False):
            request.session.set_expiry(0)
        login(request=request, user=user)
    return user


def delete_user(request: HttpRequest) -> None:
    user = request.user
    logout(request=request)
    user.delete()


def change_password(request: HttpRequest, form: forms.PasswordChangeForm):
    user = form.save()
    update_session_auth_hash(request=request, user=user)


def delete_email_verification_token(user):
    """Delete token for the user if exists"""

    models.EmailVerificationToken.objects.filter(user=user).delete()


def send_verification_email(request: HttpRequest):
    delete_email_verification_token(user=request.user)
    token = models.EmailVerificationToken.objects.create(user=request.user)
    subject = render_to_string(template_name="users/email_verification_subject.txt").strip()
    message = render_to_string(
        template_name="users/email_verification_email.html",
        context={
            "protocol": "https" if settings.EMAIL_USE_TLS else "http",
            "domain": request.get_host(),
            "uuid": token.to_string,
        },
    )
    from_email = settings.EMAIL_FROM_ADDRESS
    recipient_list = [request.user.email]
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
    )


def verify_user_email(uuid):
    """Verify user email address using the token, even if they are not logged in"""

    token = models.EmailVerificationToken.objects.filter(uuid=uuid).first()
    if not token:
        raise ValueError("Invalid token")
    if token.is_expired:
        url = reverse_lazy(viewname="users:email_verify_resend")
        msg = f"Token is expired. Please request a new verification link <a href='{url}'>here</a>"
        raise ValueError(msg)
    token.user.is_verified = True
    token.user.save()
    delete_email_verification_token(user=token.user)


def change_email(request, form):
    """Change user email address, mark email as unverified, send verification email"""

    user = form.save(commit=False)
    user.is_verified = False
    user.save()
    send_verification_email(request=request)
