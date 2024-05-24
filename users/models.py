from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

class User(AbstractUser):
    pass

class UserFile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='user_files/')
    name = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(default=timezone.now)
    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, through='SharedWith', related_name='shared_files')

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name
        super(UserFile, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class SharedWith(models.Model):
    user_file = models.ForeignKey('UserFile', related_name='shared_with_entries', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user_file', 'user')

    def __str__(self):
        return f"{self.user_file} shared with {self.user}"

    
class Comment(models.Model):
    user_file = models.ForeignKey(UserFile, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.user_file}"
    




