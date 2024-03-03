from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Follower(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='to_follow_user_id')
    follower = models.ForeignKey(User,on_delete=models.CASCADE,related_name='follower_id')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
