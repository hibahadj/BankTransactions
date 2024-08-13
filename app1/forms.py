from django import forms
from app1.models import Client, Admin ,Compte

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['clientnom', 'clientprenom', 'clientdn', 'clientemail', 'clienttelephone', 'clientadresse', 'is_active']

class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['adminusername', 'adminemail']


class CompteForm(forms.ModelForm):
    class Meta:
        model = Compte
        fields = ['client', 'comptesolde', 'comptedevise']
        # You can include other fields as needed
        # Exclude fields that should not be editable in the form