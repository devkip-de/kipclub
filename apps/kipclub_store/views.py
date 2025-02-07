from django.shortcuts import render, get_object_or_404
from .models import Product

def home_store(request):
    return render(request, 'home_kcs.html')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})
