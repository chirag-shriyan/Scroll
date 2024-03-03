from django.contrib import admin
from .models import Post,Post_Like,Post_Comment

# Register your models here.

class PostAdmin(admin.ModelAdmin):
     list_display = ["post_id", "user_id" , "file", "bio" , "is_public",'num_of_likes',"created_at","updated_at"]

admin.site.register(Post,PostAdmin)

class Post_Like_Admin(admin.ModelAdmin):
     list_display = ["post_id", "user_id","created_at","updated_at"]

admin.site.register(Post_Like,Post_Like_Admin)

class Post_Comment_Admin(admin.ModelAdmin):
     list_display = ["post_id", "user_id","comment","created_at","updated_at"]

admin.site.register(Post_Comment,Post_Comment_Admin)
