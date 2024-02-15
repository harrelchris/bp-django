from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

app_name = "users"

urlpatterns = [
    path(route="register/", view=views.register, name="register"),
    path(route="delete/", view=views.delete, name="delete"),
    path(route="login/", view=views.login, name="login"),
    path(route="logout/", view=views.logout, name="logout"),
    path(route="account/", view=views.account, name="account"),
    path(route="email/change/", view=views.email_change, name="email_change"),
    path(route="password/change/", view=views.password_change, name="password_change"),
    path(
        route="password/reset/",
        view=auth_views.PasswordResetView.as_view(
            email_template_name="users/password_reset_email.html",
            subject_template_name="users/password_reset_subject.txt",
            success_url=reverse_lazy("users:password_reset_done"),
            template_name="users/password_reset.html",
        ),
        name="password_reset",
    ),
    path(
        route="password/reset/done/",
        view=auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        route="password/reset/confirm/<uidb64>/<token>/",
        view=auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy("users:password_reset_complete"),
            template_name="users/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),
    path(
        route="password/reset/complete/",
        view=auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
