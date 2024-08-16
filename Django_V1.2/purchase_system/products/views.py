from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.forms import ModelForm
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
import pandas as pd
from django.db import IntegrityError
from django.contrib import messages
import logging
from orders.models import Order

logger = logging.getLogger(__name__)

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'code', 'quantity', 'supplier', 'image']

def product_list(request):
    products = Product.objects.all()  # استعلام لجلب جميع المنتجات
    return render(request, 'products/products_list.html', {'products': products})

def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'products/products_form.html', {'form': form})

def product_update(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.quantity = form.cleaned_data['quantity']
            logger.debug(f"Updating quantity to: {product.quantity}")
            product.save()
            messages.success(request, "Product updated successfully.")
            return redirect('product_list')
    else:
        product.refresh_from_db()  # Refresh the product instance from the database
        form = ProductForm(instance=product)
    return render(request, 'products/products_form.html', {'form': form})

def product_delete(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'products/products_confirm_delete.html', {'object': product})

def product_data(request):
    products = Product.objects.all().values('name', 'code')
    return JsonResponse(list(products), safe=False)

def product_export(request):
    products = Product.objects.all().values('code', 'name', 'stock', 'supplier')
    df = pd.DataFrame(list(products))
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="products.xlsx"'
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return response

def product_import(request):
    if request.method == 'POST' and request.FILES['product_file']:
        product_file = request.FILES['product_file']
        data = pd.read_excel(product_file)

        if 'code' not in data.columns:
            messages.error(request, "The uploaded file must contain a 'code' column.")
            return redirect('product_list')

        for index, row in data.iterrows():
            try:
                Product.objects.update_or_create(
                    code=row['code'],
                    defaults={
                        'name': row['name'],
                        'stock': row['stock'],
                        'supplier': row['supplier'],
                        'quantity': row['stock']  # Assuming you want to set stock equal to quantity on import
                    }
                )
            except IntegrityError as e:
                messages.error(request, f"Error saving product with code {row['code']}: {str(e)}")
                return redirect('product_list')

        messages.success(request, "Products imported successfully.")
        return redirect('product_list')
    else:
        return HttpResponseBadRequest("Invalid method or no file found.")

def get_current_quantity(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return JsonResponse({'current_quantity': product.quantity})

def get_or_create_order(request):
    # Example implementation, adjust according to your application's requirements
    order, created = Order.objects.get_or_create(user=request.user)

def your_submit_view(request):
    if request.method == 'POST':
        # Assuming you have a way to get or create an order, you need to define it here
        order = get_or_create_order(request)  # Replace with your actual method to retrieve or create an order
        # Save the data to the database
        return redirect('order_review', order_id=order.id)
    else:
        # Handle other cases or error
        return HttpResponseBadRequest("Invalid request")