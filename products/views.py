from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ProductForm
from .models import Product

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully!')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product_app/product_form.html', {'form': form})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_app/product_list.html', {'products': products})

def product_details(request,id):
    product_single = get_object_or_404(Product,id=id)
    return render(request, 'product_app/product_details.html', {'product': product_single})

def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_app/product_form.html', {'form': form})

def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('product_list')
