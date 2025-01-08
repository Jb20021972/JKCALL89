# Generated by Django 5.1.4 on 2025-01-08 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='pa',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name="Prix d'achat (PA)"),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products/images/', verbose_name='Image du produit'),
        ),
    ]
