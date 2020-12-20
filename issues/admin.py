from django.contrib import admin
from .models import UserProfile, Issue, Comment, Like, DisLike
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Issue)
admin.site.register(Comment)
admin.site.register(DisLike)
admin.site.register(Like)
