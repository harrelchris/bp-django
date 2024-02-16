from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse_lazy

from . import models


def delete_existing_email_verification_token(user=None, uuid=None):
    """Delete extant and unused token for the user if exists"""

    if not any([user, uuid]):
        raise ValueError("Either user or uuid is required")
    if user:
        models.EmailVerificationToken.objects.filter(user=user).delete()
    else:
        models.EmailVerificationToken.objects.filter(uuid=uuid).delete()


def send_verification_email(request):
    delete_existing_email_verification_token(user=request.user)
    token = models.EmailVerificationToken.objects.create(user=request.user)
    subject = render_to_string(template_name="users/email_verification_subject.txt").strip()
    message = render_to_string(
        template_name="users/email_verification_email.html",
        context={
            "protocol": "https" if settings.EMAIL_USE_TLS else "http",
            "domain": request.get_host(),
            "uuid": token.uuid,
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
    delete_existing_email_verification_token(uuid=uuid)


def change_email(request, form):
    """Change user email address, mark email as unverified, send verification email"""

    user = form.save(commit=False)
    user.is_verified = False
    user.save()
    send_verification_email(request=request)
