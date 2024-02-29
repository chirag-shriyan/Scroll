from django.contrib import admin
from .models import Post

# Register your models here.

class PostAdmin(admin.ModelAdmin):
     list_display = ["post_id", "user_id" , "file", "bio" , "is_public","created_at","updated_at"]

admin.site.register(Post,PostAdmin)
