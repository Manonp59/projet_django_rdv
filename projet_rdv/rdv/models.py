from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Classe pour l'utilisateur 
class User(AbstractUser):
    
    class Role(models.TextChoices):
        CLIENT = 'CLIENT'
        ADMIN = 'ADMIN'
    role = models.fields.CharField(choices=Role.choices, max_length=6, default='CLIENT')
    

# Classe pour les rendez-vous 
class Rdv(models.Model):
    
    date = models.DateTimeField(default=timezone.now(), unique=True)
    motif = models.CharField(max_length=30)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    notes = models.CharField(max_length=1000)
    
    class Meta:
        permissions = (
            ("creer_creneau","creer un nouveau creneau"),
            ("supprimer_creneau","supprimer un creneau"),
            ("ajouter_note","ajouter une note"),
            ("modifier_note", "modifier la note")
        )
    

