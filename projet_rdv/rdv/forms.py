from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from rdv.models import Rdv, User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label="Nom d'utilisateur")
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')
    
    
class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')
        
class PrendreRdv(forms.ModelForm):
    class Meta:
        model = Rdv
        exclude = ('date','user','notes',)
        
class CreerCreneau(forms.ModelForm):
    class Meta:
        model = Rdv
        exclude = ('user', 'motif', 'notes',)
        

class DeplacerRDV(forms.ModelForm):
    class Meta:
        model = Rdv
        exclude = ('user', 'motif','notes',)
        
class AjouterNotes(forms.ModelForm):
    class Meta : 
        model = Rdv
        exclude = ('user', 'motif', 'date',)

        