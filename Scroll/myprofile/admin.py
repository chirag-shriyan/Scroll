from django.contrib import admin
from .models import Follower

# Register your models here.
class FollowerAdmin(admin.ModelAdmin):
    list_display = ['user_id','follower',"created_at","updated_at"]

admin.site.register(Follower,FollowerAdmin)