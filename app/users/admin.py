from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models

admin.site.register(models.EmailVerificationToken)
admin.site.register(models.User, UserAdmin)

UserAdmin.list_display += ("is_verified",)
UserAdmin.fieldsets += (("Verification", {"fields": ("is_verified",)}),)
UserAdmin.list_filter += ("is_verified",)
