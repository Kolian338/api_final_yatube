from django.contrib import admin

from posts.models import Group, Comment, Post, Follow, User

admin.site.register(Group)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Follow)
