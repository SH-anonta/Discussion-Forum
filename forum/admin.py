from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from forum.models import User, Board, Post, Reply
from forum.forms import UserAdminChangeForm, UserAdminCreationForm

class UserAdmin(BaseUserAdmin):

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('username', 'admin')
    list_filter = ('admin',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
         ),
    )

    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()


# registrations
admin.site.register(User, UserAdmin)
admin.site.register(Board)
admin.site.register(Post)
admin.site.register(Reply)

# unregistrations
# admin.site.unregister(Group)