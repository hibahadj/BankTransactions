from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

class Client(models.Model):
    clientid = models.AutoField(primary_key=True)
    clientnom = models.CharField(max_length=255, null=True)
    clientprenom = models.CharField(max_length=255, null=True)
    clientdn = models.DateField(null=True, blank=True)
    clientemail = models.EmailField(max_length=255, null=True, blank=True)
    clienttelephone = models.CharField(max_length=20, null=True, blank=True)
    clientusername = models.CharField(max_length=255, unique=True, editable=False, null=True)
    clientpassword = models.CharField(max_length=255)
    clientadresse = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'Client'

    def save(self, *args, **kwargs):
        if not self.clientusername:
            self.clientusername = f"{self.clientprenom}.{self.clientnom}".lower()
        if not self.pk and not self.clientpassword:  # If creating a new client without a password
            self.set_password('client123')  # Default password
        super().save(*args, **kwargs)

    def set_password(self, raw_password):
        self.clientpassword = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.clientpassword)

    def __str__(self):
        return f"{self.clientprenom} {self.clientnom}"

class Compte(models.Model):
    DEVICES_CHOICES = [
        ('Euro', 'Euro'),
        ('Dinar', 'Dinar'),
        ('Dollar', 'Dollar'),
        ('Dirhem', 'Dirhem'),
    ]
    compteid = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    comptesolde = models.FloatField(null=True, blank=True)
    comptenum = models.CharField(max_length=255, unique=True, null=True, blank=True)
    comptedevise = models.CharField(max_length=10, choices=DEVICES_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"Compte {self.compteid} ({self.client.clientusername})"

    def crediter_compte(self, transactionmontant):
        self.comptesolde += transactionmontant
        self.save()
        Transaction.objects.create(compte=self, transactiontype='Crédit', transactionmontant=transactionmontant)

    def debiter_compte(self, transactionmontant):
        if transactionmontant > self.comptesolde:
            raise ValueError("Solde insuffisant")
        self.comptesolde -= transactionmontant
        self.save()
        Transaction.objects.create(compte=self, transactiontype='Débit', transactionmontant=transactionmontant)
    class Meta:
        db_table = 'Compte'
class Transaction(models.Model):
    TYPE_TRANSACTION_CHOICES = [
        ('Crédit', 'Crédit'),
        ('Débit', 'Débit'),
    ]
    transactionid = models.AutoField(primary_key=True)
    compte = models.ForeignKey(Compte, on_delete=models.CASCADE, null=True)
    transactiontype = models.CharField(max_length=10, choices=TYPE_TRANSACTION_CHOICES, null=True)
    transactionmontant = models.FloatField(null=True)
    transactiondate = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return f"Transaction {self.transactionid} ({self.transactiontype})"
    class Meta:
        db_table = 'Transaction'
class HistoriqueTransaction(models.Model):
    historiqueid = models.AutoField(primary_key=True)
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, null=True)
    compte = models.ForeignKey(Compte, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Historique {self.historiqueid} ({self.transaction.transactiontype})"
    class Meta:
        db_table = 'HistoriqueTransaction'
class Admin(models.Model):
    adminid = models.AutoField(primary_key=True)
    adminusername = models.CharField(max_length=255, unique=True)  # Ensure uniqueness
    adminpassword = models.CharField(max_length=255)  # Remove default value
    adminemail = models.CharField(max_length=255, null=True)
    last_login = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'Admin'

    def save(self, *args, **kwargs):
        if not self.pk and not self.adminpassword:  # If creating a new admin without a password
            self.set_password('admin123')  # Default password
        super().save(*args, **kwargs)

    def set_password(self, raw_password):
        self.adminpassword = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.adminpassword)

    def __str__(self):
        return self.adminusername
    
