from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.Search ,name='search'),
    path('profile/', views.My_Profile ,name='profile'),
    path('users/<str:username>', views.User_Profile),
    path('follow/', views.Handel_Follow_Req,name='follow'),

]