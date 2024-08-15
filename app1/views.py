from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib import messages
from django.views.generic import TemplateView, ListView
from django.views.decorators.csrf import csrf_protect
from app1.models import Client, Admin, Compte,Transaction
from django.contrib.auth.hashers import check_password, make_password
import json
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .forms import ClientForm, CompteForm 
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required






def delete_client(request, client_id):
    if request.method == 'POST':
        try:
            client = get_object_or_404(Client, clientid=client_id)
            client.delete()
            messages.success(request, "Client supprimer avec succès!")
        except Client.DoesNotExist:
            messages.error(request, "Client n'existe pas!")
        except Exception as e:
            messages.error(request, f'An error occurred while deleting the client: {str(e)}')
    else:
        messages.error(request, 'Invalid request method. Please use POST.')
    
    return redirect('clients')  # Redirige vers la page de liste des clients


class ListeClientsView(ListView):
    model = Client
    template_name = 'liste_clients.html'
    context_object_name = 'clients'
#comment
class ListeComptesView(ListView):
    model = Compte
    template_name = 'liste_comptes.html'
    context_object_name = 'comptes'
class SettingsView(TemplateView):
    template_name = 'settings.html'

class ClientSettingsView(TemplateView):
    template_name = 'settings_client.html'

class ListeTransactionsView(TemplateView):
    template_name = 'liste_transactions.html'

class InfoPersonelsView(TemplateView):
    template_name = 'info_personels.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user_id' in self.request.session:
            try:
                admin_user = Admin.objects.get(pk=self.request.session['user_id'])
                context['admin'] = admin_user
            except Admin.DoesNotExist:
                context['admin'] = None
        else:
            context['admin'] = None
        return context
#client template    
class ClientInfoPersonelsView(TemplateView):
    template_name = 'info_client.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user_id' in self.request.session:
            try:
                client_user = Client.objects.get(pk=self.request.session['user_id'])
                context['client'] = client_user
            except Admin.DoesNotExist:
                context['client'] = None
        else:
            context['client'] = None
        return context

def authenticate_custom_user(username, password):
    print(f"Authenticating user: {username}")
    
    try:
        admin_user = Admin.objects.get(adminusername=username)
        print(f"Admin user found: {admin_user.adminusername}")
        if check_password(password, admin_user.adminpassword):
            print("Admin password is correct")
            return admin_user
        else:
            print("Admin password is incorrect")
    except Admin.DoesNotExist:
        print("Admin user does not exist")

    try:
        client_user = Client.objects.get(clientusername=username)
        print(f"Client user found: {client_user.clientusername}")
        if check_password(password, client_user.clientpassword):
            print("Client password is correct")
            return client_user
        else:
            print("Client password is incorrect")
    except Client.DoesNotExist:
        print("Client user does not exist")
    
    print("Authentication failed")
    return None

@csrf_protect
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Attempting login for username: {username}")
        
        user = authenticate_custom_user(username, password)

        if user:
            print(f"User authenticated: {user}")
            user.last_login = timezone.now()  # Update last login time
            user.save()
           # print("User logged in successfully")

            # Manually set the session
            request.session['user_id'] = user.pk  # Custom session handling
            request.session['is_authenticated'] = True  # Custom flag for authentication
            request.session.save()
            # Verify Session Key
            session_key = request.session.session_key
            print(f"Session Key: {session_key}")

            # Ensure the session is created
            if not request.session.session_key:
                request.session.create()
            # Print all session data
            session_items = request.session.items()
            print("Session Data:")
            for key, value in session_items:
                print(f"{key}: {value}")

            # Redirect based on user type
            if isinstance(user, Admin):
                print("User is an Admin. Redirecting to admin_home.")
                return redirect('admin_home')
            elif isinstance(user, Client):
                print("User is a Client. Redirecting to client_home.")
                return redirect('client_home')
        else:
            print("Authentication failed")
            messages.error(request, "Username or Password is incorrect !!!")
            return redirect('login')

    print("Rendering login page")
    return render(request, 'login.html')

def LogoutPage(request):
    print("Logging out user")
    auth_logout(request)
    request.session.flush()  # Clear the session data
    print("Session data flushed")
    return redirect('login')

def AdminHomePage(request):
    # Check if the user is authenticated
    if 'is_authenticated' in request.session and request.session['is_authenticated']:
        # Check if the user is an Admin
        if 'user_id' in request.session:
            try:
                user = Admin.objects.get(pk=request.session['user_id'])
                print("Rendering admin_home page")
                return render(request, 'admin_home.html', {'user': user})
            except Admin.DoesNotExist:
                print("Admin user does not exist")
                return redirect('login')
        else:
            print("No user_id in session")
            return redirect('login')
    else:
        print("User is not authenticated")
        return redirect('login')

def ClientHomePage(request):
    # Check if the user is authenticated
    if request.session.get('is_authenticated'):
        # Retrieve the user from the session
        user_id = request.session.get('user_id')
        
        try:
            # Fetch the user from the database
            user = Client.objects.get(pk=user_id)
            print("Rendering client_home page")
            return render(request, 'client_home.html', {'user': user})
        except Client.DoesNotExist:
            print("Client not found in the database")
            return redirect('login')
    else:
        print("Unauthorized access to client_home")
        return redirect('login')

def CreateClient(request):
    print("Accessing CreateClient view")
    
    # Check if the user is authenticated
    if not request.session.get('is_authenticated'):
        print("Unauthorized access to CreateClient")
        return redirect('login')

    # Proceed if the user is authenticated
    if request.method == 'POST':
        clientnom = request.POST.get('clientnom')
        clientprenom = request.POST.get('clientprenom')
        clientemail = request.POST.get('clientemail')
        clienttelephone = request.POST.get('clienttelephone')
        clientadresse = request.POST.get('clientadresse')
        clientdn = request.POST.get('clientdn')
        
        print(f"Creating client: {clientnom} {clientprenom}")
        client = Client(
            clientnom=clientnom,
            clientprenom=clientprenom,
            clientemail=clientemail,
            clienttelephone=clienttelephone,
            clientadresse=clientadresse,
            clientdn=clientdn
        )
        client.set_password('client123')  # Set default password
        client.save()
        print(f"Client created with ID: {client.pk}")
        messages.success(request, "Client créer avec succès!")
        return redirect('clients')  # Redirection to the list of clients

    print("Rendering CreateClient form")
    return render(request, 'create_client.html')  # Render a form for GET requests
    

def get_client_data(request, client_id):
    client = get_object_or_404(Client, clientid=client_id)
    client_data = {
        'clientid': client.clientid,
        'clientnom': client.clientnom,
        'clientprenom': client.clientprenom,
        #'clientusername': client.clientusername,
        'clientemail': client.clientemail,
        'clienttelephone': client.clienttelephone,
        'clientadresse': client.clientadresse,
        'clientdn': client.clientdn,#.strftime('%Y-%m-%d'),  # Format date for HTML input
    }
    return JsonResponse(client_data)


def edit_client(request, client_id):
    client = get_object_or_404(Client, clientid=client_id)
    
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        
        if form.is_valid():
            # Update the clientusername before saving
            client = form.save(commit=False)  # Don't save the form data yet
            client.clientusername = f"{client.clientprenom}.{client.clientnom}".lower()
            client.save()  # Now save the updated client object
            
            messages.success(request, "Client modifier avec succès!")
            return redirect('clients')  # Redirect to the clients list
            
    else:
        form = ClientForm(instance=client)
    
    return render(request, 'edit_client.html', {'form': form, 'client': client})



@csrf_protect
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if 'user_id' in request.session:
            admin_user = Admin.objects.get(pk=request.session['user_id'])

            if not check_password(current_password, admin_user.adminpassword):
                messages.error(request, "Mot de passe actuel non valide!")
                return redirect('settings')

            if new_password != confirm_password:
                messages.error(request, "Le nouveau mot de passe et la confirmation ne correspondent pas!")
                return redirect('settings')

            # Update the password
            admin_user.set_password(new_password)
            messages.success(request, "Mot de passe modifier avec succès!")
            return redirect('settings')
    
    return redirect('settings')

@csrf_protect
def client_change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if 'user_id' in request.session:
            client_user = Client.objects.get(pk=request.session['user_id'])

            if not check_password(current_password, client_user.clientpassword):
                messages.error(request, "Mot de passe actuel non valide!")
                return redirect('clientsettings')

            if new_password != confirm_password:
                messages.error(request, "Le nouveau mot de passe et la confirmation ne correspondent pas!")
                return redirect('clientsettings')

            # Update the password
            client_user.set_password(new_password)
            messages.success(request, "Mot de passe modifier avec succès!")
            return redirect('clientsettings')
    
    return redirect('clientsettings')

def ProposClientPage(request):
    return render(request, 'proposclient.html')

def get_compte_data(request, compteid):
    compte = get_object_or_404(Compte, compteid=compteid)
    compte_data = {
        'compteid': compte.compteid,
        'client': compte.client.clientid,  # Assuming you want to include client ID, adjust as needed
        'comptesolde': str(compte.comptesolde),  # Convert to string for consistent JSON format
        'comptenum': compte.comptenum,
        'comptedevise': compte.comptedevise,
    }
    return JsonResponse(compte_data)
def create_account(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = CompteForm(request.POST)
        if form.is_valid():
            compte = form.save(commit=False)
            compte.client = client
            compte.save()
            messages.success(request, 'Compte créer avec succès!')
            return redirect('clients')
    else:
        form = CompteForm()

    return render(request, 'create_account_modal.html', {'form': form, 'client': client})

#

def delete_account(request, compte_id):
    if request.method == 'POST':
        try:
            compte = get_object_or_404(Compte, compteid=compte_id)
            compte.delete()
            messages.success(request, "Compte supprimer avec succès!")
        except Client.DoesNotExist:
            messages.error(request, "Compte n'existe pas.")
        except Exception as e:
            messages.error(request, f'An error occurred while deleting the account: {str(e)}')
    else:
        messages.error(request, 'Invalid request method. Please use POST.')
    
    return redirect('comptes')  # Redirige vers la page de liste des clients


def dashboard_view(request):

    # Récupérer les statistiques
    nombre_clients = Client.objects.count()
    nombre_comptes = Compte.objects.count()

    context = {
        'nombre_clients': nombre_clients,
        'nombre_comptes': nombre_comptes,
    }
    return render(request, 'dashboard.html', context)


def dashboard_client(request):
    # Récupérez l'ID du client à partir de la session
    client_id = request.session.get('user_id')  # Assurez-vous que 'user_id' est bien stocké dans la session

    if client_id:
        try:
            # Récupérez le client depuis la base de données
            client = Client.objects.get(pk=client_id)
            # Récupérez les comptes du client
            comptes = Compte.objects.filter(client=client)

            # Créez des données pour le graphique
            labels = [compte.comptenum for compte in comptes]
            data = [compte.comptesolde for compte in comptes]

            return render(request, 'client_dashboard.html', {
                'client': client,
                'comptes': comptes,
                'labels': labels,
                'data': data
            })
        except Client.DoesNotExist:
            return redirect('login')
    else:
        return redirect('client_dashboard')





def mescomptes(request):
    # Récupérer l'ID du client depuis la session (ou le modèle User si c'est là que vous stockez l'ID)
    user_id = request.session.get('user_id')  # Assurez-vous que l'ID du client est stocké dans la session
    
    if not user_id:
        return redirect('login')  # Rediriger si l'utilisateur n'est pas authentifié
    
    try:
        # Récupérer le client à partir de l'ID
        client = Client.objects.get(pk=user_id)
        
        # Récupérer tous les comptes associés à ce client
        comptes = Compte.objects.filter(client=client)
        
        # Rendre le template avec les comptes
        return render(request, 'mescomptes.html', {'comptes': comptes})
    
    except Client.DoesNotExist:
        # Gérer le cas où le client n'existe pas
        return redirect('login')