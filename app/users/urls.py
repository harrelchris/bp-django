from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path(route="register/", view=views.register, name="register"),
    path(route="delete/", view=views.delete, name="delete"),
    path(route="login/", view=views.login, name="login"),
    path(route="logout/", view=views.logout, name="logout"),
    path(route="account/", view=views.account, name="account"),
    path(route="email/change/", view=views.email_change, name="email_change"),
    path(
        route="email/verify/token/<uuid>/",
        view=views.email_verify,
        name="email_verify",
    ),
    path(
        route="email/verify/resend/",
        view=views.email_verify_resend,
        name="email_verify_resend",
    ),
    path(route="password/change/", view=views.password_change, name="password_change"),
    path(
        route="password/reset/",
        view=views.ResetPasswordView.as_view(),
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
        view=views.ResetPasswordConfirmView.as_view(),
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
