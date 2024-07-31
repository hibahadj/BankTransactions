from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages

# Create your views here.
@login_required(login_url='login')
@never_cache
def HomePage(request):
    return render(request, 'home.html')

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password is incorrect !!!")
            return redirect('login')  # Redirect after setting the message

    return render(request, 'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')
