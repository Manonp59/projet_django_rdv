from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    
    class Role(models.TextChoices):
        CLIENT = 'CLIENT'
        ADMIN = 'ADMIN'
    role = models.fields.CharField(choices=Role.choices, max_length=6, default='CLIENT')
    
    
class Rdv(models.Model):
    date = models.DateTimeField(default=timezone.now())
    motif = models.CharField(max_length=30)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    notes = models.CharField(max_length=300)
    
    

