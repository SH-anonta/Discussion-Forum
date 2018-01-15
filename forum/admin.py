from django.contrib import admin
from forum.models import Board, Post, Reply, UserProfile

# registrations
# admin.site.register(User, UserAdmin)
admin.site.register(Board)
admin.site.register(Post)
admin.site.register(Reply)
admin.site.register(UserProfile)
