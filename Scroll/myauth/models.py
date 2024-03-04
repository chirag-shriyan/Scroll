from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ProfilePic(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE,blank = True ,null = True)
    file = models.FileField(upload_to='profiles')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)