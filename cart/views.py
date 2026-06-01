from django.shortcuts import render, redirect, get_object_or_404

from products.models import Product
from .cart import Cart


def add_to_cart(request, product_id):

    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)

    cart.add(product=product)

    return redirect('cart_detail')


def remove_from_cart(request, product_id):

    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)

    cart.remove(product)

    return redirect('cart_detail')


def increase_quantity(request, product_id):

    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)

    cart.add(product=product, quantity=1)

    return redirect('cart_detail')


def decrease_quantity(request, product_id):

    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)

    product_id = str(product.id)

    if product_id in cart.cart:

        if cart.cart[product_id]['quantity'] > 1:

            cart.cart[product_id]['quantity'] -= 1

        else:

            cart.remove(product)

        cart.save()

    return redirect('cart_detail')


def cart_detail(request):

    cart = Cart(request)

    return render(request, 'cart/detail.html', {
        'cart': cart
    })