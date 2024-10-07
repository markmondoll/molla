from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from profiles.models import Profile

User = get_user_model()

class CustomUserAdmin(UserAdmin):
    model = User
    # Use 'username' instead of 'username'
    list_display = ['email', 'username', 'is_staff', 'is_active']

admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)