from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from rdv.models import Rdv, User
from rdv.widget import DateTimePickerInput
from django.forms import widgets


# Utilisé pour obtenir un calendrier
class DateInput(forms.DateTimeInput):
    input_type = 'date_time'


# Formulaire de connexion
class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label="Nom d'utilisateur")
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')
    

# Formulaire d'inscription 
class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')


# Formulaire de mofification du compte
class ModifCompte(forms.ModelForm):
    class Meta:
        model = User 
        fields = ('username','email', 'first_name', 'last_name',)


#Formulaire pour prendre un rendez-vous       
class PrendreRdv(forms.ModelForm):
    class Meta:
        model = Rdv
        exclude = ('date','user','notes',)
        
# Formulaire pour créer un créneau 
class CreerCreneau(forms.ModelForm):
    class Meta:
        model = Rdv
        exclude = ('user', 'motif', 'notes',)
        fields = ['date']
        widgets = {'date':widgets.DateTimeInput(attrs={'type':'datetime-local'})}
        

# Formulaire pour ajouter des notes et modifier les notes 
class AjouterNotes(forms.ModelForm):
    class Meta : 
        model = Rdv
        exclude = ('user', 'motif', 'date',)

        