from django.contrib import admin
from .models import CustomUser, Function, BusinessLocation, Profile
from django.utils.translation import gettext_lazy as _


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', '__token__', 'created_at', 'updated_at', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')})
    )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'business', 'created_at', 'function', 'updated_at', 'is_active']


@admin.register(Function)
class FunctionAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at', 'is_active']


@admin.register(BusinessLocation)
class BusinessLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at', 'is_active']

