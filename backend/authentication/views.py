from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from authentication.models import User
from authentication.serializers import RegisterSerializer, LoginSerializer, CustomUserSerializer
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
  """
  Register view for creating a new user.
  It validates the data using the RegisterSerializer.
  If valid, it creates a new user.
  If invalid or an unexpected error occurs, it returns an appropriate status code.
  """
  try:
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
      user = serializer.save()
      return Response(
        { 'message': 'Registration successful.' },
        status=status.HTTP_201_CREATED
      )
    else:
      logger.error("Registration failed due to validation errors: %s", serializer.errors)
      return Response(
        {'errors': serializer.errors, 'message': 'Registration failed.'},
        status=status.HTTP_400_BAD_REQUEST
      )
  except Exception as error:
    logger.exception("Unexpected error during registration.")
    return Response(
      {'error': 'An unexpected error occurred. Please try again later.', 'message': 'Registration failed.'},
      status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
  """
  Login view for authenticating a user.
  It validates the data using the LoginSerializer.
  If valid, it returns the user data along with tokens.
  If invalid or an unexpected error occurs, it returns an appropriate status code.
  """
  try:
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
      user = serializer.validated_data.get('user')
      token = RefreshToken.for_user(user)
      user_serializer = CustomUserSerializer(user)
      data = user_serializer.data
      data['tokens'] = {
        'refresh': str(token),
        'access': str(token.access_token),
      }
      return Response(
        {'user': data, 'message': 'Login successful.'},
        status=status.HTTP_200_OK
      )
    else:
      logger.error("Login failed due to validation errors: %s", serializer.errors)
      return Response(
        {'errors': serializer.errors, 'message': 'Login failed.'},
        status=status.HTTP_400_BAD_REQUEST
      )
  except Exception as error:
    logger.exception("Unexpected error during login.")
    return Response(
      {'error': 'An unexpected error occurred. Please try again later.', 'message': 'Login failed.'},
      status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
  """
  Logout view for logging out a user.
  It blacklists the refresh token to prevent further access.
  It returns a 205 status code if successful.
  If invalid or an unexpected error occurs, it returns an appropriate status code.
  """
  try:
    refresh_token = request.data['refresh']
    token = RefreshToken(refresh_token)
    token.blacklist()
    return Response(
      {'message': 'Logout successful.'},
      status=status.HTTP_205_RESET_CONTENT
    )
  except Exception as error:
    logger.exception("Logout failed for user %s", request.user)
    return Response(
      {'error': 'An error occurred. Please try again later.', 'message': 'Logout failed.'},
      status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user_view(request, pk):
  """
  Delete view for deleting a user account.
  It checks if the user is authenticated and has the required permissions.
  It deletes the user and returns a 204 status code if successful.
  If invalid or an unexpected error occurs, it returns an appropriate status code.
  """
  try:
    user = User.objects.get(pk=pk)
    user.delete()
    return Response(
      {'message': 'Deletion successful.'},
      status=status.HTTP_204_NO_CONTENT
    )
  except User.DoesNotExist:
    logger.error("User with pk %s not found.", pk)
    return Response(
      {'error': 'User not found', 'message': 'Deletion failed.'},
      status=status.HTTP_404_NOT_FOUND
    )
  except Exception as error:
    logger.exception("Deletion failed for user pk %s", pk)
    return Response(
      {'error': 'An error occurred. Please try again later.', 'message': 'Deletion failed.'},
      status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_view(request):
  """
  Get view for retrieving user information.
  It checks if the user is authenticated and has the required permissions.
  It returns the user data.
  If invalid or an unexpected error occurs, it returns an appropriate status code.
  """
  try:
    user = request.user
    serializer = CustomUserSerializer(user)
    return Response(
      {'user': serializer.data, 'message': 'User retrieval successful.'},
      status=status.HTTP_200_OK
    )
  except Exception as error:
    logger.exception("User retrieval failed for user %s", request.user)
    return Response(
      {'error': 'An error occurred. Please try again later.', 'message': 'User retrieval failed.'},
      status=status.HTTP_400_BAD_REQUEST
    )
