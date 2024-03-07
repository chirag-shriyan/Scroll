from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index,name='/'),
    path('get_posts', views.Get_Posts,name='get_posts'),
]