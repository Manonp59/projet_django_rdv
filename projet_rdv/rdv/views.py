from django.shortcuts import render

def accueil(request):
    return render(request, 'rdv/accueil.html')


def connexion_client(request):
    return render(request, 'connexion_client.html')

def connexion_administrateur(request):
    return render(request, 'connexion_administrateur.html')

def contact(request):
    return render(request, 'contact.html')