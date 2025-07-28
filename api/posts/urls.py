from django.urls import path 
from . import views

urlpatterns = [
    path('posts/', views.GetPostOrAddPost.as_view()),                        # POST
    path('posts/<int:id_post>/detail/', views.GetPostOrAddPost.as_view()),  # GET
    path('posts/<int:id_post>/', views.DeleteOrUpdatePost.as_view()),       # PUT e DELETE
    path('posts/feed/', views.FeedPosts.as_view())
]
