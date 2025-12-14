from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserProfileView, UserFollowView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('follow/<int:user_id>/', UserFollowView.as_view(), name='follow'),
]
