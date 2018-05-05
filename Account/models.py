from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    birthday = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(blank=True)
    def __str__(self):
        return 'UserProfile for {}'.format(self.user.username)


class UserInfo(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    school = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=50, blank=True)
    aboutme = models.TextField(blank=True)

    def __str__(self):
        return "UserInfo for {}".format(self.user.username)
