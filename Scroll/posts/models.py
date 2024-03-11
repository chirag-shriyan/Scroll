from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    post_id = models.IntegerField(primary_key = True)
    user = models.ForeignKey(User,on_delete = models.CASCADE,null = True, blank = True)
    file = models.FileField(upload_to='posts')
    bio = models.TextField()
    is_public = models.BooleanField(default = False)
    num_of_likes = models.BigIntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Post_Like(models.Model):
    post = models.ForeignKey(Post,on_delete = models.CASCADE,null = True, blank = True)
    user = models.ForeignKey(User,on_delete = models.CASCADE,null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Post_Comment(models.Model):
    post = models.ForeignKey(Post,on_delete = models.CASCADE,null = True, blank = True)
    user = models.ForeignKey(User,on_delete = models.CASCADE,null = True, blank = True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)