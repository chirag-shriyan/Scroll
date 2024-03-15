from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Message(models.Model):
    sender = models.ForeignKey(User,on_delete = models.SET_NULL,null = True,related_name='sender')
    receiver = models.ForeignKey(User,on_delete = models.SET_NULL,null = True,related_name='receiver')
    message = models.TextField()
    is_unread = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add = True)

class Chat_Room(models.Model):
    user1 = models.ForeignKey(User,on_delete = models.SET_NULL,null = True,related_name='user1')
    user2 = models.ForeignKey(User,on_delete = models.SET_NULL,null = True,related_name='user2')
    room_id = models.TextField()
    last_message = models.TextField(default = '')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Notification(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    room_id = models.TextField()
    num_of_notifications = models.IntegerField(default = 0)
    is_notification = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)