from django.contrib import admin
from users.models import User


@admin.register(User)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "phone", "city", "avatar")
    list_filter = ("city", "id", "email")
