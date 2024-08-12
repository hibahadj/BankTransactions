"""BankTransactions URL Configuration

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
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.urls import path
from app1 import views
from django.conf import settings
from app1.views import ListeClientsView, ListeComptesView, ListeTransactionsView, InfoPersonelsView, delete_client
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/login/', permanent=False), name='home_redirect'),  # Redirect to LOGIN_URL
    path('login/',views.LoginPage,name='login'),
    path('logout/',views.LogoutPage,name='logout'),
    path('admin_home/', views.AdminHomePage, name='admin_home'),
    path('client_home/', views.ClientHomePage, name='client_home'),
    path('clients/', ListeClientsView.as_view(), name='clients'),
    path('comptes/', ListeComptesView.as_view(), name='comptes'),
    path('transactions/', ListeTransactionsView.as_view(), name='transactions'),
    path('infopersonels/', InfoPersonelsView.as_view(), name='Infopersonels'),
    #path('change-password/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('create_client/', views.CreateClient, name='create_client'),
    path('delete_client/<int:client_id>/', delete_client, name='delete_client'),
    path('edit_client/<int:client_id>/',views.edit_client, name='edit_client'),


]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)