from rest_framework import serializers
from .models import ShortenedUrl

class ShortenedUrlSerializer(serializers.ModelSerializer):
  """
  Serializer for the ShortenedUrl model.
  It returns the id, original URL, short code, shortened URL, creation date, click count and user.
  """
  class Meta:
    model = ShortenedUrl
    fields = [
      'id', 
      'original_url', 
      'short_code', 
      'shortened_url', 
      'created_at', 
      'click_count', 
      'user'
    ]
    read_only_fields = ['id', 'short_code', 'created_at', 'click_count', 'user']
