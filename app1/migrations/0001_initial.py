# Generated by Django 5.0.7 on 2024-07-31 12:31

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('utilisateurId', models.AutoField(primary_key=True, serialize=False)),
                ('utilisateurusername', models.CharField(max_length=255)),
                ('utilisateurnom', models.CharField(max_length=255)),
                ('utilisateurprenom', models.CharField(max_length=255)),
                ('utilisateuremail', models.EmailField(max_length=254, unique=True)),
                ('utilisateurpassword', models.CharField(max_length=255)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='%(class)s_set', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='%(class)s_set', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Compte',
            fields=[
                ('compteId', models.AutoField(primary_key=True, serialize=False)),
                ('numéroCompte', models.CharField(max_length=255)),
                ('solde', models.DecimalField(decimal_places=2, max_digits=15)),
                ('typeDeCompte', models.CharField(max_length=255)),
                ('devise', models.CharField(max_length=3)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('utilisateur_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app1.utilisateur')),
            ],
            options={
                'verbose_name': 'Admin',
                'verbose_name_plural': 'Admins',
            },
            bases=('app1.utilisateur',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('utilisateur_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app1.utilisateur')),
                ('clientadresse', models.CharField(max_length=255)),
                ('clientcp', models.PositiveBigIntegerField()),
                ('clientdn', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('app1.utilisateur',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='HistoriqueCredit',
            fields=[
                ('historiqueId', models.AutoField(primary_key=True, serialize=False)),
                ('montant', models.DecimalField(decimal_places=2, max_digits=15)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('devise', models.CharField(max_length=3)),
                ('compte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historiques_credit', to='app1.compte')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transactionId', models.AutoField(primary_key=True, serialize=False)),
                ('typeDeTransaction', models.CharField(max_length=255)),
                ('montant', models.DecimalField(decimal_places=2, max_digits=15)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('devise', models.CharField(max_length=3)),
                ('compteDestinataire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions_destinataire', to='app1.compte')),
                ('compteSource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions_source', to='app1.compte')),
            ],
        ),
        migrations.AddField(
            model_name='compte',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comptes', to='app1.client'),
        ),
    ]