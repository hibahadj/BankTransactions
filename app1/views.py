from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from app1.models import Client, Compte, Transaction, HistoriqueTransaction
from django.views.decorators.cache import never_cache

class ListeClientsView(ListView):
    model = Client
    template_name = 'liste_clients.html'
    context_object_name = 'clients'

class ListeComptesView(TemplateView):
    template_name = 'liste_comptes.html'

class ListeTransactionsView(TemplateView):
    template_name = 'liste_transactions.html'

class InfoPersonelsView(TemplateView):
    template_name = 'info_personels.html'


#Login
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect('admin_home')
            else:
                return redirect('client_home')
        else:
            messages.error(request, "Username or Password is incorrect !!!")
            return redirect('login')

    return render(request, 'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

@login_required
def AdminHomePage(request):
    return render(request, 'admin_home.html')

@login_required
def ClientHomePage(request):
    return render(request, 'client_home.html')

@login_required
def CreateClient(request):
    if request.method == 'POST':
        clientnom = request.POST.get('clientnom')
        clientprenom = request.POST.get('clientprenom')
        clientemail = request.POST.get('clientemail')
        clienttelephone = request.POST.get('clienttelephone')
        clientdn = request.POST.get('clientdn')
        
        client = Client.objects.create(
            clientnom=clientnom,
            clientprenom=clientprenom,
            clientemail=clientemail,
            clienttelephone=clienttelephone,
            clientdn=clientdn
        )
        
        messages.success(request, "Client created successfully.")
        return redirect('admin_home')
    return redirect('admin_home')
