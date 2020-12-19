from django.contrib import admin
from .models import UserProfile, Issue, IField
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Issue)
admin.site.register(IField)