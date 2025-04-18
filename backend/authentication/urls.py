from .views import *
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
  path('register/', register_view, name='register'),
  path('login/', login_view, name='login'),
  path('logout/', logout_view, name='logout'),
  path('delete/<int:pk>/', delete_user_view, name='delete_user'),
  path('user-info/', get_user_view, name='get_user_view'),
  path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]