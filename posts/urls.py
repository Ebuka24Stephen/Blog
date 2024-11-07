from django.urls import path 
from .views import * 

urlpatterns = [
    path('', post_list, name='post_list'),
    path('create-post/', create_post, name='create_post'),
    path('my-posts/', my_posts, name='my_post'),
    path('post-detail/<int:post_id>/', post_detail, name='post_detail'),
    path('post-update/<int:post_id>/', update_post, name='post_update'),
    path('search/', search_post, name='search'),
    path('like/<int:id>/', post_like, name='like'),
    path('comment/<int:id>/', delete_comment, name='delete_comment'),
]
