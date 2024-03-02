from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.Search ,name='search'),
    path('profile/', views.User_Profile ,name='profile'),

]