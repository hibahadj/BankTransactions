# Generated by Django 4.1.13 on 2024-08-05 14:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('adminusername', models.CharField(default='admin', max_length=255, primary_key=True, serialize=False)),
                ('adminpassword', models.CharField(default='admin123', max_length=100)),
                ('adminemail', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'Admin',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('clientid', models.AutoField(primary_key=True, serialize=False)),
                ('clientnom', models.CharField(max_length=255, null=True)),
                ('clientprenom', models.CharField(max_length=255, null=True)),
                ('clientdn', models.DateField(blank=True, null=True)),
                ('clientemail', models.EmailField(blank=True, max_length=255, null=True)),
                ('clienttelephone', models.CharField(blank=True, max_length=20, null=True)),
                ('clientusername', models.CharField(editable=False, max_length=255, null=True, unique=True)),
                ('clientpassword', models.CharField(default='client123', max_length=255)),
                ('clientadresse', models.CharField(max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'Client',
            },
        ),
        migrations.CreateModel(
            name='Compte',
            fields=[
                ('compteid', models.AutoField(default=1, primary_key=True, serialize=False)),
                ('comptesolde', models.FloatField(blank=True, null=True)),
                ('comptedevise', models.CharField(blank=True, choices=[('Euro', 'Euro'), ('Dinar', 'Dinar'), ('Dollar', 'Dollar'), ('Dirhem', 'Dirhem')], max_length=10, null=True)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.client')),
            ],
            options={
                'db_table': 'Compte',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transactionid', models.AutoField(default=1, primary_key=True, serialize=False)),
                ('transactiontype', models.CharField(choices=[('Crédit', 'Crédit'), ('Débit', 'Débit')], max_length=10, null=True)),
                ('transactionmontant', models.FloatField(null=True)),
                ('transactiondate', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('compte', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.compte')),
            ],
            options={
                'db_table': 'Transaction',
            },
        ),
        migrations.CreateModel(
            name='HistoriqueTransaction',
            fields=[
                ('historiqueid', models.AutoField(default=1, primary_key=True, serialize=False)),
                ('compte', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.compte')),
                ('transaction', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.transaction')),
            ],
            options={
                'db_table': 'HistoriqueTransaction',
            },
        ),
    ]