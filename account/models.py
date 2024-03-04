from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
# Create your models here.
from .manager import UserManager


    
class NewUser(AbstractUser):
    username = None
    mobile = models.CharField(max_length=10, unique=True)
    user_bio = models.CharField(max_length=100, null=True, blank=True)
    is_verified = models.BooleanField(default=True)
    profile_picture = models.ImageField(upload_to="profile", null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []
    