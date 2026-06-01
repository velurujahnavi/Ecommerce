from django.urls import path

from .views import (
    checkout,
    payment,
    payment_success,
    order_history,
    order_detail,
)

urlpatterns = [

    path(
        'checkout/',
        checkout,
        name='checkout'
    ),

    path(
        'payment/<int:order_id>/',
        payment,
        name='payment'
    ),

    path(
        'payment-success/<int:order_id>/',
        payment_success,
        name='payment_success'
    ),

    path(
        'history/',
        order_history,
        name='order_history'
    ),

    path(
        'detail/<int:order_id>/',
        order_detail,
        name='order_detail'
    ),
]