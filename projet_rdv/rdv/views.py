from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from rdv.models import User, Rdv
from django.contrib import messages
from datetime import datetime



def accueil(request):
    """Vue pour la page d'accueil du site. Affiche des statistiques sur les rendez-vous
    à venir et les créneaux horaires libres pour la journée courante.

    Args:
        request : requête HTTP reçue par la vue

    Returns:
        - réponse HTTP avec un template rendu contenant les statistiques suivantes :
            - le nombre de rendez-vous à venir pour la journée courante
            - le nombre de créneaux horaires libres pour la journée courante
            - la date courante au format 'YYYY-MM-DD'
            - l'heure courante au format 'HH:MM'
    """
    today = datetime.now().date()
    rdv_a_venir = Rdv.objects.filter(date__gte=today, user__isnull=False)
    rdv_count = rdv_a_venir.count()
    creneaux_libres = Rdv.objects.filter(date__gte=today, user__isnull=True)
    creneaux_libres_count = creneaux_libres.count()
    now = datetime.now()
    hour = now.strftime("%H:%M")
    return render(request, 'rdv/accueil.html',{'rdv_count':rdv_count, 'creneaux_libres_count':creneaux_libres_count, 'today':today, 'hour':hour})


def login_page(request):
    """
    Vue pour la page de connexion du site. Permet à un utilisateur de se connecter avec son nom d'utilisateur
    et son mot de passe, puis redirige l'utilisateur vers la page d'accueil si les informations de connexion
    sont valides.

    Parameters:
    - request: requête HTTP reçue par la vue

    Returns:
    - réponse HTTP avec un template rendu contenant un formulaire de connexion et un message d'erreur (si applicable)
      - si le formulaire est soumis et valide, l'utilisateur est authentifié et redirigé vers la page d'accueil
      - sinon, le formulaire est réaffiché avec un message d'erreur indiquant que les identifiants sont invalides
    """
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
    """
    Vue pour la déconnexion de l'utilisateur connecté. Déconnecte l'utilisateur actuel et le redirige vers la
    page d'accueil.

    Parameters:
    - request: requête HTTP reçue par la vue

    Returns:
    - réponse HTTP avec une redirection vers la page d'accueil
    """
    logout(request)
    return redirect('accueil')


def signup_page(request):
    """
    Vue pour la page d'inscription du site. Affiche un formulaire d'inscription permettant à un nouvel utilisateur
    de créer un compte en fournissant un nom d'utilisateur, une adresse email et un mot de passe. Si le formulaire
    est soumis et valide, le nouvel utilisateur est enregistré et connecté automatiquement, puis redirigé vers la
    page d'accueil.

    Parameters:
    - request: requête HTTP reçue par la vue

    Returns:
    - réponse HTTP avec un template rendu contenant un formulaire d'inscription
      - si le formulaire est soumis et valide, un nouvel utilisateur est créé et connecté, puis l'utilisateur est
        redirigé vers la page d'accueil
      - sinon, le formulaire est réaffiché avec les erreurs de validation appropriées
    """
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
    """
    Vue pour la prise d'un rendez-vous sur un créneau horaire libre. Affiche un formulaire permettant à l'utilisateur
    connecté de choisir un motif de rendez-vous, puis enregistre le rendez-vous avec le motif choisi et l'utilisateur
    connecté. Redirige ensuite l'utilisateur vers la liste de ses rendez-vous à venir.

    Parameters:
    - request: requête HTTP reçue par la vue
    - id: identifiant du créneau horaire sur lequel prendre rendez-vous

    Returns:
    - réponse HTTP avec un template rendu contenant un formulaire de prise de rendez-vous
      - si le formulaire est soumis et valide, un nouveau rendez-vous est créé avec l'utilisateur connecté et le motif
        choisi, puis l'utilisateur est redirigé vers la liste de ses rendez-vous à venir
      - sinon, le formulaire est réaffiché avec les erreurs de validation appropriées
    """
    user = request.user
    rdv = Rdv.objects.get(id=id)
    form = forms.PrendreRdv(request.POST)
    if request.method == 'POST':
        form = forms.PrendreRdv(request.POST, instance = rdv)
        rdv.user = user
        rdv.motif = request.POST['motif']
        rdv.save()
        messages.success(request, 'Votre rendez-vous a bien été enregistré ✅')
        return redirect('mes-rdv')
    else : 
        form = forms.PrendreRdv(request.POST, instance = rdv)
    return render(request, 'rdv/prendre_rdv.html', {'form':form , 'rdv':rdv})


@login_required(login_url='login')
def user_detail(request):
    """
    Vue affichant les détails de l'utilisateur connecté (nom d'utilisateur, adresse e-mail, etc.) ainsi que
    certaines actions qu'il peut effectuer (modifier son mot de passe, supprimer son compte, etc.).

    Parameters:
    - request: requête HTTP reçue par la vue

    Returns:
    - réponse HTTP avec un template rendu contenant les détails de l'utilisateur connecté et les actions possibles
    """
    return render(request, 'rdv/mon-compte.html')


@login_required(login_url='login')
def modifier_compte(request):
    """
    Fonction de vue qui permet à un utilisateur connecté de modifier les informations de son compte.

    Si la méthode HTTP de la requête est 'POST', les données du formulaire sont validées et enregistrées,
    et l'utilisateur est redirigé vers l'URL 'mon-compte'. Si la méthode n'est pas 'POST', le formulaire est
    initialisé avec les données de l'utilisateur actuel et affiché sur le modèle 'modifier-mon-compte'.

    Args:
        request: L'objet de requête HTTP envoyé par le client.

    Returns:
        Un objet de réponse HTTP qui contient le modèle 'modifier-mon-compte' rendu avec l'objet de formulaire
        comme données de contexte.
    """
    user = request.user
    if request.method == 'POST':
        form = forms.ModifCompte(request.POST, instance = user)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Vos modifications ont bien été prises en compte ✅')
            return redirect('mon-compte')

    else : 
        form = forms.ModifCompte(instance = user)
    return render(request, 'rdv/modifier-mon-compte.html', {'form':form})


@login_required(login_url='login')
def liste_rdv(request):
    """
    Fonction de vue qui affiche une liste de rendez-vous.

    Cette fonction utilise le décorateur @login_required pour vérifier si l'utilisateur est connecté. Si l'utilisateur
    n'est pas connecté, il sera redirigé vers l'URL 'login'.

    La fonction récupère tous les objets Rdv (c'est-à-dire tous les rendez-vous) à partir de la base de données, puis les
    envoie au modèle 'mes-rdv.html' pour les afficher.

    Args:
        request: L'objet de requête HTTP envoyé par le client.

    Returns:
        Un objet de réponse HTTP qui contient le modèle 'mes-rdv.html' rendu avec la liste de rendez-vous en tant que
        données de contexte.
    """
    liste_rdv = Rdv.objects.all()
    return render(request, 'rdv/mes-rdv.html', {'liste_rdv':liste_rdv})


@login_required(login_url='login')
def rdv_detail(request, id):
    """
    Fonction de vue qui affiche les détails d'un rendez-vous.

    Cette fonction utilise le décorateur @login_required pour vérifier si l'utilisateur est connecté. Si l'utilisateur
    n'est pas connecté, il sera redirigé vers l'URL 'login'.

    La fonction récupère l'objet Rdv correspondant à l'ID donné à partir de la base de données, puis l'envoie au modèle
    'rdv-detail.html' pour l'afficher.

    Args:
        request: L'objet de requête HTTP envoyé par le client.
        id: L'ID du rendez-vous à afficher.

    Returns:
        Un objet de réponse HTTP qui contient le modèle 'rdv-detail.html' rendu avec l'objet Rdv correspondant à l'ID
        en tant que données de contexte.

    Raises:
        Rdv.DoesNotExist: si l'ID donné ne correspond à aucun rendez-vous dans la base de données.
    """
    rdv = Rdv.objects.get(id=id)
    return render(request, 'rdv/rdv-detail.html', {'rdv':rdv})


@login_required(login_url='login')
def rdv_delete(request, id):
    """
    Supprime un rendez-vous spécifié par son identifiant et redirige l'utilisateur vers la liste de ses rendez-vous.
    
    Paramètres :
    request : HttpRequest
        La requête HTTP reçue par la vue.
    id : int
        L'identifiant du rendez-vous à supprimer.
        
    Retour :
    HttpResponse
        La réponse HTTP renvoyée à l'utilisateur.
    """
    rdv_to_delete = Rdv.objects.get(id=id)
    if request.method == 'POST':
        rdv = Rdv()
        rdv.date = rdv_to_delete.date
        rdv_to_delete.delete()
        rdv.save()
        messages.success(request, "Le rendez-vous a bien été supprimé ✅")
        return redirect('mes-rdv')
        
    
    return render(request, 'rdv/supprimer-rdv.html', {'rdv_to_delete':rdv_to_delete})


@permission_required('rdv.creer_creneau', raise_exception=True)
@login_required(login_url='login')
def creer_creneau(request):
    """
    Affiche un formulaire pour créer un créneau de rendez-vous disponible, et enregistre le créneau s'il est valide.

    Requiert l'autorisation 'rdv.creer_creneau'.

    Paramètres :
    request : HttpRequest
        La requête HTTP reçue par la vue.

    Retour :
    HttpResponse
        La réponse HTTP renvoyée à l'utilisateur.
    """
    form = forms.CreerCreneau(request.POST)
    if request.method == 'POST':
        form = forms.CreerCreneau(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Le créneau a bien été créé ✅')
            return redirect('creneaux-dispo')
        else :
            messages.warning(request,'Ce créneau est déjà créé ❌')
    return render(request, 'rdv/admin/creer-creneaux.html', {'form' : form})


@login_required(login_url='login')
def creneaux_dispo(request):
    """
    Affiche la liste des créneaux de rendez-vous disponibles à partir de maintenant.

    Paramètres :
    request : HttpRequest
        La requête HTTP reçue par la vue.

    Retour :
    HttpResponse
        La réponse HTTP renvoyée à l'utilisateur.
    """
    liste_rdv = Rdv.objects.filter(date__gte = datetime.now())
    return render(request, 'rdv/creneaux-dispo.html', {'liste_rdv':liste_rdv})


@permission_required('rdv.ajouter_note', raise_exception=True)
@login_required(login_url='login')
def ajouter_notes(request, id):
    """
    Affiche un formulaire pour ajouter des notes à un rendez-vous spécifié par son identifiant, et enregistre les notes si elles sont valides.

    Requiert l'autorisation 'rdv.ajouter_note'.

    Paramètres :
    request : HttpRequest
        La requête HTTP reçue par la vue.
    id : int
        L'identifiant du rendez-vous auquel ajouter les notes.

    Retour :
    HttpResponse
        La réponse HTTP renvoyée à l'utilisateur.
    """
    rdv = Rdv.objects.get(id=id)
    form = forms.AjouterNotes(request.POST)
    if request.method == 'POST':
        form = forms.AjouterNotes(request.POST)
        if form.is_valid():
            rdv.notes = request.POST['notes']
            rdv.save()
            messages.success(request, 'Les notes ont été enregistrées ✅')
            return redirect('rdv-detail', rdv.id)
    return render(request, 'rdv/admin/ajouter-notes.html', {'form' : form, 'rdv':rdv})


@permission_required('rdv.supprimer_creneau', raise_exception=True)
@login_required(login_url='login')
def supprimer_creneau(request, id):
    """
    Supprime un créneau de rendez-vous spécifié par son identifiant.

    Requiert l'autorisation 'rdv.supprimer_creneau'.

    Paramètres :
    """
    rdv = Rdv.objects.get(id=id)
    if request.method == 'POST':
        rdv.delete()
        messages.success(request, "Le rendez-vous a bien été supprimé ✅")
        return redirect('creneaux-dispo')
        
    
    return render(request, 'rdv/admin/supprimer-creneau.html', {'rdv':rdv})


@permission_required('rdv.modifier_note', raise_exception=True)
@login_required(login_url='login')
def modifier_note(request, id):
    """
    Affiche un formulaire pour modifier les notes d'un rendez-vous spécifié par son identifiant, et enregistre les modifications si elles sont valides.

    Requiert l'autorisation 'rdv.modifier_note'.

    Paramètres :
    request : HttpRequest
        La requête HTTP reçue par la vue.
    id : int
        L'identifiant du rendez-vous à modifier.

    Retour :
    HttpResponse
        La réponse HTTP renvoyée à l'utilisateur.
    """
    rdv = Rdv.objects.get(id=id)
    if request.method == 'POST':
        form = forms.AjouterNotes(request.POST, instance = rdv)
        
        if form.is_valid():
            rdv = form.save()
            messages.success(request, 'Vos modifications ont bien été enregistrées ✅')
            return redirect('rdv-detail', rdv.id)

    else : 
        form = forms.AjouterNotes(instance = rdv)
    return render(request, 'rdv/admin/modifier-note.html', {'rdv':rdv , 'form':form})






    



