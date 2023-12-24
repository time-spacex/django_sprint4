from django.urls import path, include

from . import views


app_name = 'blog'

urlpatterns: list = [
    path('', include('users.urls')),
    path('', views.index, name='index'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/',
         views.category_posts,
         name='category_posts'),
    path('posts/create/', views.post_create, name='create_post'),
    path('posts/<int:post_id>/edit/', views.post_edit, name='edit_post'),
    path('posts/<int:post_id>/delete/', views.post_delete, name='delete_post'),
    path('posts/<int:post_id>/comment/', views.coment_create, name='add_comment'),
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/', views.coment_edit, name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/', views.coment_delete, name='delete_comment'),
]
