from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from reviews.forms import ReviewForm


def product_list(request):
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()

    category_slug = request.GET.get('category')
    search_query = request.GET.get('q')

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if search_query:
        products = products.filter(name__icontains=search_query)

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_slug,
    })


def product_detail(request, slug):
    product = get_object_or_404(
        Product,
        slug=slug,
        available=True
    )

    form = ReviewForm()

    return render(request, 'products/product_detail.html', {
        'product': product,
        'form': form,
    })