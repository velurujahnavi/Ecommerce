from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

import razorpay

from django.conf import settings

from cart.cart import Cart

from .forms import OrderCreateForm

from .models import Order, OrderItem


@login_required
def checkout(request):

    cart = Cart(request)

    if len(cart) == 0:

        return render(
            request,
            'orders/order_success.html',
            {
                'order': None
            }
        )

    if request.method == 'POST':

        form = OrderCreateForm(request.POST)

        if form.is_valid():

            order = form.save(commit=False)

            order.user = request.user

            order.save()

            for item in cart:

                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            cart.clear()

            return redirect(
                'payment',
                order_id=order.id
            )

    else:

        form = OrderCreateForm(
            initial={
                'email': request.user.email
            }
        )

    return render(
        request,
        'orders/checkout.html',
        {
            'cart': cart,
            'form': form
        }
    )


@login_required
def payment(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id
    )

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    amount = 50000

    razorpay_order = client.order.create({

        'amount': amount,

        'currency': 'INR',

        'payment_capture': '1'

    })

    return render(
        request,
        'orders/payment.html',
        {
            'order': order,
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_key': settings.RAZORPAY_KEY_ID,
            'amount': amount,
        }
    )


@login_required
def payment_success(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id
    )

    payment_id = request.GET.get(
        'razorpay_payment_id'
    )

    if payment_id:

        order.payment_id = payment_id

        order.paid = True

        order.save()

    return render(
        request,
        'orders/payment_success.html',
        {
            'order': order
        }
    )


@login_required
def order_history(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'orders/order_history.html',
        {
            'orders': orders
        }
    )
@login_required
def order_detail(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        'orders/order_detail.html',
        {
            'order': order
        }
    )    