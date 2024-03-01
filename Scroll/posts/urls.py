from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.Create_Posts ,name='posts'),
    path('posts/<int:post_id>', views.Post_view),
]