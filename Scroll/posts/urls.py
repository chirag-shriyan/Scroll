from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.Create_Posts ,name='posts'),
    path('get_posts', views.Get_Posts,name='get_posts'),
    path('posts/<int:post_id>', views.Post_View),
    path('edit_posts/<int:post_id>', views.Post_Edit),
    path('post_delete/', views.Post_Delete,name='post_delete'),
    path('likes/', views.Like_Posts,name='likes'),
    path('comments/', views.Comment_Posts,name='comments'),
]