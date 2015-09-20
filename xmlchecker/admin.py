from django.contrib import admin

# Register your models here.

from .models import UserFile, Errors

admin.site.register(UserFile)
admin.site.register(Errors)