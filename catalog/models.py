
from django.utils import timezone
import uuid
from django.db import models
from django.urls import reverse


class AuthTable(models.Model):
    
    # Поля
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100)
    user_email = models.EmailField()
    pssword = models.CharField(max_length=200)
    reg_time = models.DateTimeField(auto_now_add=True)
    # …

    # # Метаданные
    # class Meta:
    #     pass


    # # Methods
    # def get_absolute_url(self):
    #     return reverse('model-detail-view', args=[str(self.user_id)])

    # def __str__(self):
    #     return self.my_field_name
    

class OwnDocTable(models.Model):
    # Поля
    doc_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey('AuthTable', on_delete=models.CASCADE)
    file_name = models.CharField(max_length=100)
    #file = models
    status = models.CharField(max_length=20)
    # …

    # # Метаданные
    # class Meta:
    #     pass


    # # Methods
    # def get_absolute_url(self):
    #     return reverse('model-detail-view', args=[str(self.doc_id)])

    # def __str__(self):
    #     return self.my_field_name


class ForeignDocTable(models.Model):
    # Поля
    foreign_doc_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey('AuthTable', on_delete=models.CASCADE)
    foreign_user_id = models.CharField(max_length=100)
    file_name = models.CharField(max_length=20)
    # …

    # Метаданные
    # class Meta:
    #     pass


    # # Methods
    # def get_absolute_url(self):
    #     return reverse('model-detail-view', args=[str(self.foreign_doc_id)])

    # def __str__(self):
    #     return self.my_field_name
    

class StatusTable(models.Model):
    # Поля
    foreign_user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doc_id = models.ForeignKey('OwnDocTable', on_delete=models.CASCADE)
    foreign_user_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    # …

    # # Метаданные
    # class Meta:
    #     pass


    # # Methods
    # def get_absolute_url(self):
    #     return reverse('model-detail-view', args=[str(self.foreign_user_id)])

    # def __str__(self):
    #     return self.my_field_name


class CommentTable(models.Model):
    # Поля
    comment_id = models.UUIDField(default=uuid.uuid4, editable=False)
    foreign_user_id = models.ForeignKey('StatusTable', on_delete=models.CASCADE)
    comments = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    # …

    # # Метаданные
    # class Meta:
    #     pass


    # # Methods
    # def get_absolute_url(self):
    #     return reverse('model-detail-view', args=[str(self.comment_id)])

    # def __str__(self):
    #     return self.my_field_name

