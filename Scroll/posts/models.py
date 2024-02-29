from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    post_id = models.IntegerField(primary_key = True)
    user = models.ForeignKey(User,on_delete = models.CASCADE,null = True, blank = True)
    file = models.FileField(upload_to='posts')
    bio = models.CharField(max_length=50)
    is_public = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)