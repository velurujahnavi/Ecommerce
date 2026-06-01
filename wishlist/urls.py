from django.urls import path
from .views import (
    add_to_wishlist,
    wishlist_detail,
    remove_from_wishlist,
)

urlpatterns = [
    path('', wishlist_detail, name='wishlist_detail'),
    path('add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove/<int:item_id>/', remove_from_wishlist, name='remove_from_wishlist'),
]