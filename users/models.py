from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class UserFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='user_files/')

    def __str__(self):
        return self.name