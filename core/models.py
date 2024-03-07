from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

from npunto import settings

class Activity(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=[('done', 'Done'), ('pending', 'Pending')], default='pending')
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  


    def __str__(self):
        return self.name



class ActivityUpdate(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    status = models.CharField(max_length=10)
    remark = models.TextField(blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    
    



class Staffuser(AbstractUser):
    position = models.CharField(max_length=100, null=True, blank=True)
    contact = models.IntegerField(null=True, blank=True)