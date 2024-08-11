from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import Admin, Client, Compte, Transaction, HistoriqueTransaction
from app1.forms import ClientForm, AdminForm

class ClientAdmin(admin.ModelAdmin):
    form = ClientForm

class AdminAdmin(admin.ModelAdmin):
    form = AdminForm

# Register the models with the custom admin classes
admin.site.register(Admin, AdminAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Compte)
admin.site.register(Transaction)
admin.site.register(HistoriqueTransaction)
