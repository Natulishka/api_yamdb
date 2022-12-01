from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'password', 'role', 'is_superuser',
                    'is_staff', 'is_active')
    search_fields = ('username', 'email')
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
