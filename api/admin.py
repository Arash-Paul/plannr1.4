from django.contrib import admin
from .models import User, CreatedEvent
from django.contrib.auth.models import Group
from .forms import UserAdminCreationForm, UserAdminChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'full_name', 'admin', 'staff', 'active')
    list_filter = ('admin', 'staff', 'active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('full_name', 'gender', 'profile_picture')}),
        ('Permissions', {'fields': ('admin', 'staff', 'active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
            },
        )
    )
    search_fields = ('email','full_name',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(CreatedEvent)
# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)
