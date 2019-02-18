from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'nickname', 'date_joined')
    search_fields = ('email', 'username', 'nickname')
    list_filter = ('date_joined',)

