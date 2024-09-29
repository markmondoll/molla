from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from profiles.models import Profile

User = get_user_model()

class CustomUserAdmin(UserAdmin):
    model = User
    # Use 'user_name' instead of 'username'
    list_display = ['email', 'user_name', 'is_staff', 'is_active']

admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)