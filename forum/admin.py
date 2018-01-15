from django.contrib import admin
from forum.models import Board, Post, Reply

#todo delete
#
# class UserAdmin(BaseUserAdmin):
#
#     form = UserAdminChangeForm
#     add_form = UserAdminCreationForm
#
#     list_display = ('username', 'admin')
#     list_filter = ('admin',)
#
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         ('Personal info', {'fields': ()}),
#         ('Permissions', {'fields': ('admin',)}),
#     )
#
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'password1', 'password2')}
#          ),
#     )
#
#     search_fields = ('username',)
#     ordering = ('username',)
#     filter_horizontal = ()


# registrations
# admin.site.register(User, UserAdmin)
admin.site.register(Board)
admin.site.register(Post)
admin.site.register(Reply)

# unregistrations
# admin.site.unregister(Group)