from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
class ListeClientsView(TemplateView):
    template_name = 'liste_clients.html'

class ListeComptesView(TemplateView):
    template_name = 'liste_comptes.html'

class ListeTransactionsView(TemplateView):
    template_name = 'liste_transactions.html'

class InfoPersonelsView(TemplateView):
    template_name = 'info_personels.html'


# Create your views here.
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirection basée sur le rôle de l'utilisateur
            if user.is_superuser:
                return redirect('admin_home')
            else:
                return redirect('client_home')
        else:
            messages.error(request, "Username or Password is incorrect !!!")
            return redirect('login')  # Redirection après avoir défini le message

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
