from django.urls import path
from . import views

urlpatterns = [
    path('lobby/',views.Lobby,name='lobby'),
    path('chats/<str:username>',views.Chat_Room,),
]