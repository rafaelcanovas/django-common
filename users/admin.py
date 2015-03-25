from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdmin_
from django.utils.translation import ugettext as _

from users.models import User
from users.forms import UserSignupForm, UserChangeForm


class UserAdmin(UserAdmin_):
    list_display = ('email', 'full_name', 'is_staff')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('full_name',)}),
        (_('Permissions'), {'fields': (
            'is_active', 'is_verified', 'is_staff',
            'is_superuser', 'groups', 'user_permissions'
        )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password'),
        }),
    )
    form = UserChangeForm
    add_form = UserSignupForm


admin.site.register(User, UserAdmin)
