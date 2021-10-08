from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=3)
    location = models.CharField(max_length=55)
    isDonor = models.BooleanField(default=False, blank=True)
    profile_pic = models.ImageField(upload_to='profile/')
