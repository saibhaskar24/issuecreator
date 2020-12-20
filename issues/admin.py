from django.contrib import admin
from .models import UserProfile, Issue, Comment, CLike, CDisLike, ILike, IDisLike
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Issue)
admin.site.register(Comment)
admin.site.register(CDisLike)
admin.site.register(CLike)
admin.site.register(IDisLike)
admin.site.register(ILike)
