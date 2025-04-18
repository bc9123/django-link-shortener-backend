from .views import *
from django.urls import path

urlpatterns = [
  path('user-urls/', get_user_urls, name='get_user_urls'),
  path('shorten-url/', shorten_url, name='shorten_url'),
  path('delete-url/<str:short_code>/', delete_url, name='delete_url'),
]