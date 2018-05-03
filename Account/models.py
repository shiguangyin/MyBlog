from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    birthday = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return 'UserProfile for {}'.format(self.user.username)
