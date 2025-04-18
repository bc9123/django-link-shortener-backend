from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from shortener.views import redirect_url

urlpatterns = [
  path('<str:short_code>', redirect_url, name='redirect_url'),
  path('authentication/', include('authentication.urls')),
  path('shortener/', include('shortener.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)