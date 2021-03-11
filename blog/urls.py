from . import views
from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, CommentCreateView, CommentUpdateView, CommentDeleteView

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/comment/new/',
         CommentCreateView.as_view(), name='comment-create'),
    path('post/<int:post_pk>/comment/<int:pk>/update/',
         CommentUpdateView.as_view(), name='comment-update'),
    path('post/<int:post_pk>/comment/<int:pk>/delete/',
         CommentDeleteView.as_view(), name='comment-delete'),
    path('about/', views.about, name='blog-about'),
]
