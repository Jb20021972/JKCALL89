# Generated by Django 5.1.4 on 2025-01-06 21:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name="Nom de l'opérateur")),
                ('country', models.CharField(max_length=100, verbose_name='Pays')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='operators/', verbose_name="Logo de l'opérateur")),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nom du produit')),
                ('value', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valeur du produit')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Prix de vente')),
                ('stock', models.IntegerField(default=0, verbose_name='Stock disponible')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.operator')),
            ],
        ),
    ]
