from django.urls import path
from . import views

urlpatterns = [
    path('operators/', views.operator_list, name='operator_list'),  # Liste des opérateurs
    path('products/<int:operator_id>/', views.product_list, name='product_list'),  # Produits par opérateur
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),  # Détail d'un produit
]
