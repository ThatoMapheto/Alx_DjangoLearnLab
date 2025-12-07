from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Main pages
    path('', views.PostListView.as_view(), name='post_list'),

    # Post CRUD - Updated to match checker requirements
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(),
         name='post_update'),  # Changed from 'edit' to 'update'
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

    # Comments
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),

    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

    # Tagging and Search
    path('tag/<str:tag_name>/', views.posts_by_tag, name='posts_by_tag'),
    path('search/', views.search_posts, name='search_posts'),
]
