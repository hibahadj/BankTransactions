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
from app1.views import ListeClientsView, ListeComptesView, ListeTransactionsView, InfoPersonelsView, SettingsView, delete_client, change_password, client_change_password, ClientInfoPersonelsView, ClientSettingsView, ProposClientPage, delete_account, dashboard_view, create_transaction, download_transactions, ListeTransactionsClientView, transfer_funds
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
    path('clientinfopersonels/', ClientInfoPersonelsView.as_view(), name='clientinfopersonels'),
    path('settings/', SettingsView.as_view(), name='settings'),
    path('clientsettings/', ClientSettingsView.as_view(), name='clientsettings'),
    path('change-password/', change_password, name='change_password'),
    path('client-change-password/', client_change_password, name='client_change_password'),
    path('create_client/', views.CreateClient, name='create_client'),
    path('delete_client/<int:client_id>/', delete_client, name='delete_client'),
    path('delete_account/<int:compte_id>/', delete_account, name='delete_account'),
    path('edit_client/<int:client_id>/',views.edit_client, name='edit_client'),
    path('get_client_data/<int:client_id>/', views.get_client_data, name='get_client_data'),
    path('create_account/<int:client_id>/', views.create_account, name='create_account'),
    path('create_transaction/<int:compte_id>/', create_transaction, name='create_transaction'),
    path('propos/', ProposClientPage, name='proposclient'),  
    path('get_compte_data/<int:compteid>/', views.get_compte_data, name='get_compte_data'),
    path('download_transactions/<str:compte_num>/', download_transactions, name='download_transactions'),
    path('dashboard', dashboard_view, name='dashboard'),
    path('client_dashboard/', views.dashboard_client, name='client_dashboard'),
    path('mescomptes/', views.mescomptes, name='mescomptes'),
    path('transactionClient/', ListeTransactionsClientView.as_view(), name='transactionClient'),
    path('transfer_funds/', transfer_funds, name='transfer_funds'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)