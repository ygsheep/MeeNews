from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'nickname', 'is_active', 'is_staff', 'is_verified')
    search_fields = ('username', 'email', 'nickname')
