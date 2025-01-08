from django.contrib import admin
from .models import Operator, Product

@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    """
    Configuration de l'affichage des opérateurs dans l'interface admin.
    """
    list_display = ('name', 'country', 'logo')  # Ajout de la colonne logo
    search_fields = ('name', 'country')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Configuration de l'affichage des produits dans l'interface admin.
    """
    list_display = ('name', 'operator', 'value', 'price', 'pa', 'marge', 'marge_percentage', 'stock', 'updated_at')
    search_fields = ('name', 'operator__name')
    list_filter = ('operator',)

    def marge(self, obj):
        """
        Affiche la marge calculée (PV - PA).
        """
        return f"{obj.marge:.2f} €" if obj.pa else "N/A"

    def marge_percentage(self, obj):
        """
        Affiche le pourcentage de marge calculé.
        """
        return f"{obj.marge_percentage:.2f} %" if obj.pa else "N/A"

    marge.short_description = 'Marge (€)'
    marge_percentage.short_description = 'Marge (%)'
