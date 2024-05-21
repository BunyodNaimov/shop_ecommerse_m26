from django.urls import path

from users.views import CreateUserAPIView, UserLoginAPIView, UserProfileAPIView

urlpatterns = [
    path('register/', CreateUserAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
]
