from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  """
  Custom user model that uses email as the unique identifier instead of username.
  """
  email = models.EmailField(unique=True)
  REQUIRED_FIELDS = ['username', 'password']
  USERNAME_FIELD = 'email'
  
  def __str__(self):
    return self.email