from rest_framework import serializers
from authentication.models import User

class CustomUserSerializer(serializers.ModelSerializer):
  """
  Serializer for the custom user model.
  It returns the user id, email, username, password and ensures the password is write-only..
  """
  class Meta:
    model = User
    fields = ('id', 'email', 'username', 'password')
    extra_kwargs = {
      'password': {'write_only': True}
    }

class RegisterSerializer(serializers.ModelSerializer):
  """
  Serializer for user registration.
  It validates the email, username and password fields.
  It ensures that the password is at least 8 characters long and matches the confirmation password.
  """
  password1 = serializers.CharField(write_only=True)
  password2 = serializers.CharField(write_only=True)
  
  class Meta:
    model = User
    fields = ('id', 'email', 'username', 'password1', 'password2')
    extra_kwargs = {
      'password1': {'write_only': True},
      'password2': {'write_only': True}
    }

  def validate(self, attrs):
    if attrs['password1'] != attrs['password2']:
      raise serializers.ValidationError("Passwords do not match.")
    
    passwords = attrs.get('password1', '')
    if len(passwords) < 8:
      raise serializers.ValidationError("Password must be at least 8 characters long.")
    return attrs

  def create(self, validated_data):
    password = validated_data.pop('password1')
    validated_data.pop('password2')
    user = User.objects.create_user(**validated_data, password=password)
    return user

class LoginSerializer(serializers.ModelSerializer):
  """
  Serializer for user login.
  It validates the email and password fields.
  It ensures that the email exists and the password is correct.
  It returns the user object if the credentials are valid.
  """
  class Meta:
    model = User
    fields = ('email', 'password')
    extra_kwargs = {
      'password': {'write_only': True}
    }

  email = serializers.EmailField()
  password = serializers.CharField(write_only=True)
  
  def validate(self, attrs):
    email = attrs.get('email')
    password = attrs.get('password')

    if not User.objects.filter(email=email).exists():
      raise serializers.ValidationError("Email does not exist.")

    user = User.objects.get(email=email)

    if not user.check_password(password):
      raise serializers.ValidationError("Incorrect password.")

    attrs['user'] = user
    return attrs

