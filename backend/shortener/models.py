import random
import string
from django.conf import settings
from django.db import models

class ShortenedUrl(models.Model):
  """
  Model for storing shortened URLs.
  It contains the original URL, shortened code, shortened URL, click count, creation date and user.
  It has a method to generate an unique short code and save the model instance.
  It has a many-to-one relationship with the user model (many shortened URLs can belong to one user).
  """
  original_url = models.URLField(max_length=100000)
  short_code = models.CharField(max_length=10, unique=True, blank=True)
  shortened_url = models.URLField(max_length=100000, blank=True)
  click_count = models.PositiveIntegerField(default=0)
  created_at = models.DateTimeField(auto_now_add=True)
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL, 
    null=True, 
    blank=True, 
    on_delete=models.SET_NULL
  )

  def generate_short_code(self):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

  def save(self, *args, **kwargs):
    if not self.short_code:
      while True:
        new_code = self.generate_short_code()
        if not ShortenedUrl.objects.filter(short_code=new_code).exists():
          self.short_code = new_code
          break
    super().save(*args, **kwargs)
