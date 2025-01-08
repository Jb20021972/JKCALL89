from django.db import models
from django.conf import settings

class Operator(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom de l'opérateur")
    country = models.CharField(max_length=100, verbose_name="Pays")
    logo = models.ImageField(upload_to='operators/', blank=True, null=True, verbose_name="Logo de l'opérateur")

    def __str__(self):
        return f"{self.name} ({self.country})"

class Product(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=100, verbose_name="Nom du produit")
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valeur du produit")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix de vente")  # PV
    pa = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Prix d'achat (PA)")  # PA
    stock = models.IntegerField(default=0, verbose_name="Stock disponible")
    is_active = models.BooleanField(default=True, verbose_name="Actif")  # Nouveau champ pour activer/désactiver
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='products/images/', null=True, blank=True, verbose_name="Image du produit")

    @property
    def marge(self):
        """
        Calcul de la marge : PV - PA
        """
        if self.pa:
            return self.price - self.pa
        return 0

    @property
    def marge_percentage(self):
        """
        Calcul du pourcentage de marge : (Marge / PA) * 100
        """
        if self.pa and self.pa > 0:
            return (self.marge / self.pa) * 100
        return 0

    def decrease_stock(self, quantity):
        """
        Diminue le stock du produit d'une certaine quantité.
        Désactive le produit si le stock atteint zéro.
        """
        if quantity > self.stock:
            raise ValueError("Stock insuffisant pour cette quantité.")
        self.stock -= quantity
        if self.stock == 0:
            self.is_active = False  # Désactive le produit si stock à zéro
        self.save()

    def increase_stock(self, quantity):
        """
        Augmente le stock du produit d'une certaine quantité.
        Réactive le produit si le stock devient positif.
        """
        self.stock += quantity
        if self.stock > 0:
            self.is_active = True  # Réactive le produit si stock positif
        self.save()

    def __str__(self):
        return f"{self.name} - {self.operator.name}"
