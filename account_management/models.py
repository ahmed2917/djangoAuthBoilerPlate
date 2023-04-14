from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

#Two extra fields added in User table by extending User model
class MyUser(AbstractUser):
    otp = models.CharField(max_length=10, blank=True)
    expires_in = models.DateTimeField(default=timezone.now())
