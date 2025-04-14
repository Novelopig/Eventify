from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        "username",
        "email",
        "date_joined",
        "is_admin",
        "is_staff",
        "is_superuser",
    )
    list_filter = ("is_admin", "is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email")
    ordering = ("username",)

    readonly_fields = ("date_joined",)

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (
            "Permissions",
            {"fields": ("is_admin", "is_staff", "is_superuser", "is_active")},
        ),
        ("Important dates", {"fields": ("date_joined",)}),
    )

    filter_horizontal = ()

    exclude = ("groups", "user_permissions")


admin.site.register(User, CustomUserAdmin)
