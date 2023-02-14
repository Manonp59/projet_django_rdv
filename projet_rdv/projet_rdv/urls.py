"""projet_rdv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import rdv.views as views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accueil/', views.accueil, name='accueil'),
    path('login/', views.login_page, name='login'), 
    path('logout/', views.logout_user, name='logout'), 
    path('signup/', views.signup_page, name='signup'),
    path('prendre-rdv/<int:id>/', views.prendre_rdv, name='prendre-rdv'), 
    path('mon-compte/', views.user_detail, name='mon-compte'),
    path('mon-compte/modifier/', views.modifier_compte, name='modifier-mon-compte'), 
    path('rdv/<int:id>/', views.rdv_detail, name='rdv-detail'),
    # path('rdv/<int:id>/modifier/', views.rdv_update, name='modifier-rdv'),
    path('rdv/<int:id>/supprimer/', views.rdv_delete, name='supprimer-rdv'),
    path('mes-rdv/', views.liste_rdv, name='mes-rdv'),  
    path('creer-creneau/', views.creer_creneau, name='creer-creneau'),
    path('creneaux-dispo/', views.creneaux_dispo, name='creneaux-dispo'), 
    path('rdv/<int:id>/notes/', views.ajouter_notes, name='ajouter-notes'), 
    path('supprimer-creneau/<int:id>/', views.supprimer_creneau, name='supprimer-creneau'), 
    path('modifier-note/<int:id>/', views.modifier_note, name='modifier-note')
    
]



