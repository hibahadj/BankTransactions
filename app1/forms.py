from django import forms
from app1.models import Client, Admin

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['clientnom', 'clientprenom', 'clientdn', 'clientemail', 'clienttelephone', 'clientadresse', 'is_active']

class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['adminusername', 'adminemail']
