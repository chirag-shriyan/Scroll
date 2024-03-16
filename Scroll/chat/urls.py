from django.urls import path
from . import views

urlpatterns = [
    path('lobby/',views.Lobby,name='lobby'),
    path('chats/<str:username>',views.Chat_Room,),
    path('add_messages/',views.Add_Messages, name='add_messages'),
    path('notifications/',views.Notifications, name='notifications'),
    path('clear_notifications/',views.Clear_Notifications, name='clear_notifications'),
    path('get_room_ids/',views.Get_Room_Id, name='get_room_ids'),
]