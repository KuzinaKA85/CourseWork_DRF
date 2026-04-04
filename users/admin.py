from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "phone_number",
        "avatar",
        "country",
        "is_active",
        "is_staff",
        "is_superuser",
        "telegram_chat_id",
    )
    list_filter = (
        "email",
        "country",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    search_fields = ("email", "country")
