from django.contrib import admin
from .models import ProfilePic

# Register your models here.

class ProfilePicAdmin(admin.ModelAdmin):
    list_display = ['user_id','file']

admin.site.register(ProfilePic,ProfilePicAdmin)