from django.conf import settings

"""
Method for building short url.
"""
def build_short_url(short_code: str) -> str:
  domain = settings.DEFAULT_DOMAIN.rstrip('/')
  return f"{domain}/{short_code}"