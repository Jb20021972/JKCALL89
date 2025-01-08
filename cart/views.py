from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import CartItem

@login_required
def add_to_cart(request, product_id):
    """
    Ajoute un produit au panier. Si le produit existe déjà dans le panier,
    incrémente simplement la quantité.
    Diminue le stock correspondant.
    """
    product = get_object_or_404(Product, id=product_id)
    
    # Vérifie que le stock est suffisant
    if product.stock < 1:
        messages.error(request, f"Le produit {product.name} est en rupture de stock.")
        return redirect('cart_detail')

    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        # Vérifie si le stock peut couvrir la nouvelle quantité
        if cart_item.quantity + 1 > product.stock:
            messages.error(request, f"Stock insuffisant pour ajouter une unité de {product.name}.")
        else:
            cart_item.quantity += 1
            cart_item.save()
            product.decrease_stock(1)
            messages.success(request, f"La quantité de {product.name} a été augmentée dans votre panier.")
    else:
        cart_item.quantity = 1
        cart_item.save()
        product.decrease_stock(1)
        messages.success(request, f"{product.name} a été ajouté à votre panier.")
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    """
    Affiche les détails du panier de l'utilisateur connecté.
    """
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

@login_required
def remove_from_cart(request, cart_item_id):
    """
    Supprime un article du panier et restitue le stock correspondant.
    """
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    product = cart_item.product
    product.stock += cart_item.quantity
    product.save()
    cart_item.delete()
    messages.success(request, f"{product.name} a été retiré de votre panier.")
    return redirect('cart_detail')

@login_required
def update_cart_quantity(request, cart_item_id):
    """
    Met à jour la quantité d'un article dans le panier et ajuste le stock.
    """
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    product = cart_item.product
    if 'quantity' in request.POST:
        try:
            new_quantity = int(request.POST['quantity'])
            if new_quantity > 0:
                # Calcul de la différence entre l'ancienne et la nouvelle quantité
                difference = new_quantity - cart_item.quantity

                if difference > 0:  # Si on augmente la quantité
                    if difference > product.stock:
                        messages.error(request, f"Stock insuffisant pour mettre à jour {product.name}.")
                    else:
                        cart_item.quantity = new_quantity
                        cart_item.save()
                        product.decrease_stock(difference)
                        messages.success(request, f"La quantité de {product.name} a été mise à jour.")
                else:  # Si on diminue la quantité
                    cart_item.quantity = new_quantity
                    cart_item.save()
                    product.stock += abs(difference)
                    product.save()
                    messages.success(request, f"La quantité de {product.name} a été mise à jour.")
            else:
                messages.warning(request, "La quantité doit être supérieure à zéro.")
        except ValueError:
            messages.error(request, "Quantité invalide.")
    return redirect('cart_detail')

@login_required
def validate_cart(request):
    """
    Vue pour valider le panier.
    """
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        messages.error(request, "Votre panier est vide.")
        return redirect('cart_detail')

    # Supposons qu'une validation réussie vide le panier.
    for item in cart_items:
        item.delete()

    messages.success(request, "Votre commande a été validée avec succès. Merci pour votre achat !")
    return redirect('operator_list')  # Redirection vers la liste des opérateurs
