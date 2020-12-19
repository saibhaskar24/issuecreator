from django.contrib import admin
from .models import UserProfile, Issue
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Issue)
