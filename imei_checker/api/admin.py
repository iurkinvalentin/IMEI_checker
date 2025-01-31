from django.contrib import admin
from .models import AllowedUser


@admin.register(AllowedUser)
class AllowedUserAdmin(admin.ModelAdmin):
    list_display = ("user_id", "username", "added_at")
    search_fields = ("user_id", "username")