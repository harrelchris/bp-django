from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe

from . import forms, services


def register(request):
    if request.method == "POST":
        form = forms.RegisterForm(data=request.POST)
        if form.is_valid():
            services.register_user(request=request, form=form)
            messages.success(
                request=request,
                message="Account created. An email has been sent to verify your account.",
            )
            return redirect(to=reverse_lazy(viewname=settings.LOGIN_REDIRECT_URL))
    else:
        form = forms.RegisterForm()
    return TemplateResponse(
        request=request,
        template="users/register.html",
        context={
            "form": form,
        },
    )


def login(request):
    if request.method == "POST":
        form = forms.LoginForm(request=request, data=request.POST)
        if form.is_valid():
            services.login_user(request=request, form=form)
            return redirect(to=reverse_lazy(viewname=settings.LOGIN_REDIRECT_URL))
    else:
        form = forms.LoginForm(request=request)
    return TemplateResponse(
        request=request,
        template="users/login.html",
        context={
            "form": form,
        },
    )


def logout(request):
    auth_logout(request)
    return redirect(to=reverse_lazy(settings.LOGOUT_REDIRECT_URL))


@login_required
def account(request):
    return TemplateResponse(
        request=request,
        template="users/account.html",
    )


@login_required
def delete(request):
    if request.method == "POST":
        services.delete_user(request=request)
        messages.success(request=request, message="Account deleted")
        return redirect(to=reverse_lazy(viewname=settings.LOGOUT_REDIRECT_URL))
    return TemplateResponse(
        request=request,
        template="users/delete.html",
    )


@login_required
def email_change(request):
    if request.method == "POST":
        form = forms.EmailChangeForm(data=request.POST, instance=request.user)
        if form.is_valid():
            services.change_email(request=request, form=form)
            messages.success(
                request=request,
                message="Email updated. A new verification link was sent.",
            )
            return redirect(to=reverse_lazy(viewname=settings.LOGIN_REDIRECT_URL))
    else:
        form = forms.EmailChangeForm()
    return TemplateResponse(
        request=request,
        template="users/email_change.html",
        context={
            "form": form,
        },
    )


def email_verify(request, uuid):
    try:
        services.verify_user_email(uuid=uuid)
    except ValueError as e:
        messages.error(request=request, message=mark_safe(e))
    else:
        messages.success(request=request, message="Your email has been verified.")
    return redirect(to=reverse_lazy(viewname=settings.LOGIN_REDIRECT_URL))


@login_required
def email_verify_resend(request):
    services.send_verification_email(request=request)
    messages.success(
        request=request,
        message="A new verification link has been sent to your email address.",
    )
    return redirect(to=reverse_lazy(viewname=settings.LOGIN_REDIRECT_URL))


@login_required
def password_change(request):
    if request.method == "POST":
        form = forms.ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            services.change_password(request=request, form=form)
            messages.success(request=request, message="Password changed")
            return redirect(to=reverse_lazy(viewname=settings.LOGIN_REDIRECT_URL))
    else:
        form = forms.ChangePasswordForm(user=request.user)
    return TemplateResponse(
        request=request,
        template="users/password_change.html",
        context={
            "form": form,
        },
    )


class ResetPasswordView(PasswordResetView):
    email_template_name = "users/password_reset_email.html"
    form_class = forms.ResetPasswordForm
    subject_template_name = "users/password_reset_subject.txt"
    success_url = reverse_lazy("users:password_reset_done")
    template_name = "users/password_reset.html"


class ResetPasswordConfirmView(PasswordResetConfirmView):
    form_class = forms.ResetPasswordConfirmForm
    success_url = reverse_lazy("users:password_reset_complete")
    template_name = "users/password_reset_confirm.html"
