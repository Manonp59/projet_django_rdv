from django.contrib import admin

from rdv.models import User,Rdv

admin.site.register([Rdv, User])
