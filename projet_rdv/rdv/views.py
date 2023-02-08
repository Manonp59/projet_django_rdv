from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from rdv.models import User, Rdv
from django.contrib import messages
from datetime import datetime



def accueil(request):
    return render(request, 'rdv/accueil.html')


def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('accueil')
            else:
                message = 'Identifiants invalides.'
    return render(
        request, 'rdv/login.html', context={'form': form, 'message': message})

@login_required(login_url='login')
def logout_user(request):
    
    logout(request)
    return redirect('accueil')


def signup_page(request):
    form = forms.SignUpForm()
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accueil')
    return render(request, 'rdv/signup.html', {'form':form})


@login_required(login_url='login')
def prendre_rdv(request, id):
    user = request.user
    rdv = Rdv.objects.get(id=id)
    form = forms.PrendreRdv(request.POST)
    if request.method == 'POST':
        form = forms.PrendreRdv(request.POST, instance = rdv)
        rdv.user = user
        rdv.motif = request.POST['motif']
        rdv.save()
        return redirect('mes-rdv')
    else : 
        form = forms.PrendreRdv(request.POST, instance = rdv)
    return render(request, 'rdv/prendre_rdv.html', {'form':form , 'rdv':rdv})



@login_required(login_url='login')
def user_detail(request):
    return render(request, 'rdv/mon-compte.html')



@login_required(login_url='login')
def modifier_compte(request):
    user = request.user
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST, instance = user)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('mon-compte')

    else : 
        form = forms.SignUpForm(instance = user)
    return render(request, 'rdv/modifier-mon-compte.html', {'form':form})



@login_required(login_url='login')
def rdv_list(request):
    liste_rdv = Rdv.objects.all()
    return render(request, 'rdv/mes-rdv.html', {'liste_rdv':liste_rdv})



@login_required(login_url='login')
def rdv_detail(request, id):
    rdv = Rdv.objects.get(id=id)
    return render(request, 'rdv/rdv-detail.html', {'rdv':rdv})

# def rdv_update(request, id):
#     rdv = Rdv.objects.get(id=id)
#     if request.method == 'POST':
#         form = forms.PrendreRdv(request.POST, instance = rdv)
        
#         if form.is_valid():
#             rdv = form.save()
#             messages.success(request,"Le rendez-vous a bien été modifié.")
#             return redirect ('rdv-detail', rdv.id )
    
#     else : 
#         form = forms.PrendreRdv(instance = rdv)
#     return render(request, 'rdv/modifier-rdv.html', {'form':form})



@login_required(login_url='login')
def rdv_delete(request, id):
    rdv_to_delete = Rdv.objects.get(id=id)
    if request.method == 'POST':
        rdv = Rdv()
        rdv.date = rdv_to_delete.date
        rdv.save()
        rdv_to_delete.delete()
        messages.success(request, "Le rendez-vous a bien été supprimé.")
        return redirect('mes-rdv')
        
    
    return render(request, 'rdv/supprimer-rdv.html', {'rdv_to_delete':rdv_to_delete})

@login_required(login_url='login')
def liste_rdv(request):
    liste_rdv = Rdv.objects.all()
    return render(request, 'rdv/admin/liste-rdv.html', {'liste_rdv':liste_rdv})



@login_required(login_url='login')
def creneaux(request):
    liste_rdv = Rdv.objects.filter(date__gte = datetime.now())
    return render(request, 'rdv/admin/creneaux.html', {'liste_rdv':liste_rdv})


@login_required(login_url='login')
def creer_creneau(request):
    form = forms.CreerCreneau(request.POST)
    if request.method == 'POST':
        form = forms.CreerCreneau(request.POST)
        if form.is_valid():
            form.save()
            return redirect('creneaux')
    return render(request, 'rdv/admin/creer-creneaux.html', {'form' : form})



@login_required(login_url='login')
def creneaux_dispo(request):
    liste_rdv = Rdv.objects.filter(date__gte = datetime.now())
    return render(request, 'rdv/creneaux-dispo.html', {'liste_rdv':liste_rdv})



@login_required(login_url='login')
def ajouter_notes(request, id):
    rdv = Rdv.objects.get(id=id)
    form = forms.AjouterNotes(request.POST)
    if request.method == 'POST':
        form = forms.AjouterNotes(request.POST)
        if form.is_valid():
            rdv.notes = request.POST['notes']
            rdv.save()
            return redirect('rdv-detail', rdv.id)
    return render(request, 'rdv/admin/ajouter-notes.html', {'form' : form, 'rdv':rdv})



@login_required(login_url='login')
def supprimer_creneau(request, id):
    rdv = Rdv.objects.get(id=id)
    if request.method == 'POST':
        rdv.delete()
        messages.success(request, "Le rendez-vous a bien été supprimé.")
        return redirect('creneaux')
        
    
    return render(request, 'rdv/admin/supprimer-creneau.html', {'rdv':rdv})




    



