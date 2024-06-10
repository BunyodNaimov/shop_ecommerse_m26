from django.urls import path

from users.views import CreateUserAPIView, UserLoginAPIView, UserProfileAPIView, CustomTokenObtainPairView

urlpatterns = [
    path('register/', CreateUserAPIView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
]
