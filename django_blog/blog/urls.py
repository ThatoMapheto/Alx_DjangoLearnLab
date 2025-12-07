from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Main pages
    path('', views.PostListView.as_view(), name='post_list'),

    # Post CRUD
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

    # Comment CRUD
    path('post/<int:pk>/comments/new/',
         views.CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/update/',
         views.CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/',
         views.CommentDeleteView.as_view(), name='comment_delete'),

    # Keep old URLs for backward compatibility
    path('comment/<int:pk>/create/',
         views.CommentCreateView.as_view(), name='comment_create_old'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:pk>/delete_func/',
         views.delete_comment, name='delete_comment_func'),

    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

    # Tagging and Search - Updated to match checker requirements
    path('tags/<slug:tag_slug>/',
         views.PostByTagListView.as_view(), name='posts_by_tag'),
    path('tag/<str:tag_name>/', views.posts_by_tag,
         name='posts_by_tag_old'),  # Keep old one
    path('search/', views.search_posts, name='search_posts'),
]
