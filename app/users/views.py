from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy

from . import forms

User = get_user_model()


def register(request):
    if request.method == "POST":
        form = forms.RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request=request, user=user)
            messages.success(request=request, message="Account created")
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
            user = authenticate(
                request=request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user:
                if not form.cleaned_data.get("remember", False):
                    request.session.set_expiry(0)
                auth_login(request=request, user=user)
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
        user = request.user
        auth_logout(request=request)
        user.delete()
        messages.success(request=request, message="Account deleted")
        return redirect(to=reverse_lazy(viewname=settings.LOGOUT_REDIRECT_URL))
    return TemplateResponse(
        request=request,
        template="users/delete.html",
    )


@login_required
def email_change(request):
    if request.method == "POST":
        form = forms.EmailChangeForm(
            data=request.POST,
            instance=request.user,
        )
        if form.is_valid():
            form.save()
            messages.success(request=request, message="Email changed")
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


@login_required
def password_change(request):
    if request.method == "POST":
        form = forms.ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request=request, user=user)
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
