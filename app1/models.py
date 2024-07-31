from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _

class Utilisateur(AbstractUser):
    utilisateurId = models.AutoField(primary_key=True)
    utilisateurusername = models.CharField(max_length=255)
    utilisateurnom = models.CharField(max_length=255)
    utilisateurprenom = models.CharField(max_length=255)
    utilisateuremail = models.EmailField(unique=True)
    utilisateurpassword = models.CharField(max_length=255)

    # Override the groups and user_permissions fields to avoid conflicts
    groups = models.ManyToManyField(
        Group,
        related_name='%(class)s_set',  # Unique related_name
        blank=True,
        help_text=_('The groups this user belongs to.'),
        verbose_name=_('groups')
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='%(class)s_set',  # Unique related_name
        blank=True,
        help_text=_('Specific permissions for this user.'),
        verbose_name=_('user permissions')
    )

    def save(self, *args, **kwargs):
        # Only hash the password if it’s being set for the first time
        if not self.pk and self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def seConnecter(self):
        pass

class Admin(Utilisateur):
    class Meta:
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'

    def créerCompte(self, client_data, compte_data):
        client = Client.objects.create(
            utilisateurnom=client_data['nom'],
            utilisateurprenom=client_data['prenom'],
            utilisateuremail=client_data['email'],
            utilisateurmp=make_password(client_data['password']),
            clientadresse=client_data['adresse']
        )
        Compte.objects.create(
            client=client,
            numéroCompte=compte_data['numéroCompte'],
            solde=compte_data['solde'],
            typeDeCompte=compte_data['typeDeCompte'],
            devise=compte_data['devise']
        )

    def désactiverCompte(self, compte_id):
        compte = Compte.objects.get(pk=compte_id)
        compte.is_active = False
        compte.save()

    def créditerCompte(self, compte_id, montant):
        compte = Compte.objects.get(pk=compte_id)
        compte.créditer(montant)

    def modifierInformationsClient(self, client_id, new_data):
        client = Client.objects.get(pk=client_id)
        for key, value in new_data.items():
            if hasattr(client, key):
                setattr(client, key, value)
        client.save()

class Client(Utilisateur):
    clientadresse = models.CharField(max_length=255)
    clientcp = models.PositiveBigIntegerField()
    clientdn = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.username:  # Generate username if it's not already set
            self.username = f"{self.utilisateurprenom[0].upper()}.{self.utilisateurnom.upper()}"
        super().save(*args, **kwargs)
    
    def consulterInformationsClient(self):
        return {
            'nom': self.utilisateurnom,
            'prenom': self.utilisateurprenom,
            'email': self.utilisateuremail,
            'date de naissance': self.clientdn,
            'adresse': self.clientadresse,
            'code postal': self.clientcp
        }

    def consulterSolde(self):
        return self.comptes.all().values('numéroCompte', 'solde', 'typeDeCompte', 'devise')

    def envoyerArgent(self, montant, destinataire_compte_id):
        compte_source = self.comptes.first()
        compte_destinataire = Compte.objects.get(pk=destinataire_compte_id)
        if compte_source.solde >= montant:
            Transaction.objects.create(
                typeDeTransaction='debit',
                montant=montant,
                compteSource=compte_source,
                compteDestinataire=compte_destinataire,
                devise=compte_source.devise
            ).exécuterTransaction()

    def recevoirArgent(self, montant, source_compte_id):
        compte_source = Compte.objects.get(pk=source_compte_id)
        compte_destinataire = self.comptes.first()
        Transaction.objects.create(
            typeDeTransaction='credit',
            montant=montant,
            compteSource=compte_source,
            compteDestinataire=compte_destinataire,
            devise=compte_source.devise
        ).exécuterTransaction()

    def imprimerInformationsRelevésCompte(self):
        return self.comptes.first().historiques_credit.all().values('montant', 'date', 'devise')

class Compte(models.Model):
    compteId = models.AutoField(primary_key=True)
    numéroCompte = models.CharField(max_length=255)
    solde = models.DecimalField(max_digits=15, decimal_places=2)
    typeDeCompte = models.CharField(max_length=255)
    devise = models.CharField(max_length=3)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='comptes')
    is_active = models.BooleanField(default=True)

    def créditer(self, montant):
        self.solde += montant
        self.save()

    def débiter(self, montant):
        if self.solde >= montant:
            self.solde -= montant
            self.save()

class Transaction(models.Model):
    transactionId = models.AutoField(primary_key=True)
    typeDeTransaction = models.CharField(max_length=255)
    montant = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    compteSource = models.ForeignKey(Compte, related_name='transactions_source', on_delete=models.CASCADE)
    compteDestinataire = models.ForeignKey(Compte, related_name='transactions_destinataire', on_delete=models.CASCADE)
    devise = models.CharField(max_length=3)

    def exécuterTransaction(self):
        if self.typeDeTransaction == 'credit':
            self.compteDestinataire.créditer(self.montant)
        elif self.typeDeTransaction == 'debit':
            self.compteSource.débiter(self.montant)
        self.save()

class HistoriqueCredit(models.Model):
    historiqueId = models.AutoField(primary_key=True)
    compte = models.ForeignKey(Compte, on_delete=models.CASCADE, related_name='historiques_credit')
    montant = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    devise = models.CharField(max_length=3)

    def enregistrerCredit(self):
        self.save()

# Create your models here.
