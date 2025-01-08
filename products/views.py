from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Operator, Product

def operator_list(request):
    """
    Vue pour afficher la liste des opérateurs.
    """
    operators = Operator.objects.all()
    return render(request, 'products/operator_list.html', {'operators': operators})

def product_list(request, operator_id):
    """
    Vue pour afficher la liste des produits actifs d'un opérateur spécifique.
    """
    operator = get_object_or_404(Operator, id=operator_id)
    products = Product.objects.filter(operator=operator, is_active=True)  # Filtre uniquement les produits actifs
    return render(request, 'products/product_list.html', {'operator': operator, 'products': products})

def product_detail(request, product_id):
    """
    Vue pour afficher les détails d'un produit actif spécifique.
    """
    try:
        product = get_object_or_404(Product, id=product_id, is_active=True)  # Assure que le produit est actif
    except Http404:
        return render(request, 'products/product_not_found.html', status=404)  # Redirige vers une page produit introuvable

    return render(request, 'products/product_detail.html', {'product': product})
