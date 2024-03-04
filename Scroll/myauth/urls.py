from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('signup/', views.Signup,name='signup'),
    path('login/', views.Login,name='login'),
    path('logout/', views.Logout,name='logout'),

    # For forgot password
    path('accounts/login/', views.Login),
]