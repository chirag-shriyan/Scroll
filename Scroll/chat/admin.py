from django.contrib import admin
from .models import Message,Chat_Room,Notification

# Register your models here.

class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender','receiver',"message","is_unread","created_at"]

admin.site.register(Message,MessageAdmin)

class Chat_RoomAdmin(admin.ModelAdmin):
    list_display = ['user1','user2',"room_id","last_message","created_at","updated_at"]

admin.site.register(Chat_Room,Chat_RoomAdmin)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user',"room_id","num_of_notifications","is_notification","created_at","updated_at"]

admin.site.register(Notification,NotificationAdmin)
