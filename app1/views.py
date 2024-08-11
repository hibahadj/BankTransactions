from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from django.contrib import messages
from django.views.generic import TemplateView, ListView
from django.views.decorators.csrf import csrf_protect
from app1.models import Client, Admin
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


def delete_client(request, client_id):
    if request.method == 'POST':
        try:
            client = get_object_or_404(Client, clientid=client_id)
            client.delete()
            messages.success(request, "Client deleted successfully.")
        except Client.DoesNotExist:
            messages.error(request, 'Client does not exist.')
        except Exception as e:
            messages.error(request, f'An error occurred while deleting the client: {str(e)}')
    else:
        messages.error(request, 'Invalid request method. Please use POST.')
    
    return redirect('clients')  # Redirige vers la page de liste des clients


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
        messages.success(request, "Client created successfully.")
        return redirect('clients')  # Redirection to the list of clients

    print("Rendering CreateClient form")
    return render(request, 'create_client.html')  # Render a form for GET requests

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth and date_of_birth > date.today():
            raise ValidationError("La date de naissance ne peut pas être supérieure à la date actuelle.")
        return date_of_birth
    