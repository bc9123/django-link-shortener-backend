from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .utils import build_short_url
from .models import ShortenedUrl
from .serializers import ShortenedUrlSerializer

"""
Gets the shortened URLs for the authenticated user.
If the user is not authenticated, it returns a 401 Unauthorized response.
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_urls(request):
  user = request.user
  urls = ShortenedUrl.objects.filter(user=user)
  serializer = ShortenedUrlSerializer(urls, many=True)
  return Response(serializer.data, status=status.HTTP_200_OK)

"""
Creates a shortened URL for the given original URL.
If the user is authenticated, it associates the shortened URL with the user.
If the user is not authenticated, it creates a public shortened URL that is not associated with any user.
If the original URL already exists for the user, it returns the existing shortened URL.
If the original URL does not exist, it creates a new shortened URL.
If the URL is valid, it returns the shortened URL.
If the URL is invalid, it returns a 400 Bad Request response with the validation errors.
"""
@api_view(['POST'])
@permission_classes([AllowAny])
def shorten_url(request):
  serializer = ShortenedUrlSerializer(data=request.data)
  if serializer.is_valid():
    user = request.user if request.user.is_authenticated else None
    existing_url = ShortenedUrl.objects.filter(
      original_url=serializer.validated_data['original_url'],
      user=user
    ).first()
    if user and existing_url:
      full_short_url = build_short_url(existing_url.short_code)
      return Response({
        'original_url': existing_url.original_url,
        'shortened_url': full_short_url
      }, status=status.HTTP_200_OK)

    shortened_url = ShortenedUrl.objects.create(
      original_url=serializer.validated_data['original_url'],
      user=user
    )

    full_short_url = build_short_url(shortened_url.short_code)

    shortened_url.shortened_url = full_short_url
    shortened_url.save()

    return Response({
      'original_url': shortened_url.original_url,
      'shortened_url': full_short_url
    }, status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
Deletes the shortened URL associated with the authenticated user.
If the user is not authenticated, it returns a 401 Unauthorized response.
If the short code does not exist, it returns a 404 Not Found response.
"""
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_url(request, short_code):
  try:
    shortened_url = ShortenedUrl.objects.get(short_code=short_code, user=request.user)
    shortened_url.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
  except ShortenedUrl.DoesNotExist:
    return Response({'error': 'Shortened URL not found'}, status=status.HTTP_404_NOT_FOUND)

"""
Redirects to the original URL based on the short code provided.
If the short code does not exist, it returns a 404 Not Found response.
"""
@renderer_classes([])
def redirect_url(request, short_code):
  try:
    shortened_url = ShortenedUrl.objects.get(short_code=short_code)
    shortened_url.click_count += 1
    shortened_url.save()
    return HttpResponseRedirect(shortened_url.original_url)
  except ShortenedUrl.DoesNotExist:
    return Response({'error': 'Shortened URL not found'}, status=status.HTTP_404_NOT_FOUND)
