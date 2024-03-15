from django.urls import path
from . import views

urlpatterns = [
    path('lobby/',views.Lobby,name='lobby'),
    path('chats/<str:username>',views.Chat_Room,),
    path('add_messages/',views.Add_Messages, name='add_messages'),
    path('notifications/',views.Notifications, name='notifications'),
]