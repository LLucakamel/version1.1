from django.shortcuts import render, redirect, get_object_or_404
from .models import Order
from products.models import Product
from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
import datetime
from django.utils import timezone
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from Projects.models import Project  # Ensure the 'projects' app is included in your Django settings

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['product_name', 'product_code', 'quantity', 'project_name', 'project_code', 'order_name', 'project_phase', 'project_consultant', 'project_location', 'request_date', 'supply_date']
        widgets = {
            'request_date': forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date().isoformat()}),
            'supply_date': forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date().isoformat()}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_name'].widget.attrs.update({'class': 'autocomplete'})
        self.fields['product_code'].widget.attrs.update({'class': 'autocomplete'})
        self.fields['project_name'].widget.attrs.update({'class': 'autocomplete'})
        self.fields['project_code'].widget.attrs.update({'class': 'autocomplete'})
        # Set the default value for request_date to today's date if it's a new form
        if not self.instance.pk:  # Checking if the instance is not saved (i.e., it's new)
            self.fields['request_date'].initial = timezone.now().date()

    def clean(self):
        cleaned_data = super().clean()
        product_name = cleaned_data.get('product_name')
        product_code = cleaned_data.get('product_code')
        if not product_name or not product_code:
            raise ValidationError("Both product name and code are required.")
        try:
            product = Product.objects.get(name=product_name, code=product_code)
        except Product.DoesNotExist:
            raise ValidationError("Product not found. Please enter a valid product name and code.")
        return cleaned_data

    def clean_quantity(self):
        product_name = self.cleaned_data.get('product_name')
        product_code = self.cleaned_data.get('product_code')
        quantity = self.cleaned_data.get('quantity')
        try:
            product = Product.objects.get(name=product_name, code=product_code)
            if quantity > product.stock:
                raise ValidationError(f"Only {product.stock} available. Cannot order more than that.")
        except Product.DoesNotExist:
            pass  # This will be handled in the clean method
        return quantity
    
    def clean_supply_date(self):
        supply_date = self.cleaned_data.get('supply_date')
        today = timezone.now().date()
        if supply_date and supply_date < today:
            raise ValidationError("Supply date cannot be in the past.")
        return supply_date
    
def order_list(request):
    orders = Order.objects.all().order_by('-request_date')
    print(f"Total orders in database: {Order.objects.count()}")
    print(f"Orders being sent to template: {len(orders)}")
    return render(request, 'orders/orders_list.html', {'orders': orders})

def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.requester = request.user  # Set the current user as the requester
            order.save()
            # Assuming you have product fields in your form
            product_name = request.POST.get('product_name')
            product_code = request.POST.get('product_code')
            quantity = request.POST.get('quantity')
            # Create or get product instance
            product, created = Product.objects.get_or_create(name=product_name, defaults={'code': product_code, 'quantity': quantity})
            order.products.add(product)
            return redirect('order_review', order_id=order.id)
        else:
            return render(request, 'orders/orders_form.html', {'form': form})
    else:
        form = OrderForm(initial={'due_date': timezone.now().date()})
        return render(request, 'orders/orders_form.html', {'form': form, 'range_1_to_10': range(1, 11)})

def order_update(request, id):
    order = get_object_or_404(Order, id=id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'orders/orders_form.html', {'form': form, 'range_1_to_10': range(1, 11)})


def order_approve(request, id):
    order = get_object_or_404(Order, id=id)
    order.status = 'approved'
    order.save()
    return redirect('order_list')

def order_disapprove(request, id):
    order = get_object_or_404(Order, id=id)
    order.status = 'disapproved'
    order.save()
    return redirect('order_list')

def product_search(request):
    term = request.GET.get('term', '')
    field = request.GET.get('field', 'name')
    if field == 'name':
        products = Product.objects.filter(name__icontains=term)[:10]
    else:
        products = Product.objects.filter(code__icontains=term)[:10]
    results = [{'label': f"{p.name} ({p.code})", 'value': p.id, 'name': p.name, 'code': p.code} for p in products]
    return JsonResponse(results, safe=False)

def project_search(request):
    term = request.GET.get('term', '')
    projects = Project.objects.filter(name__icontains=term)
    project_list = [
        {
            'name': project.name,
            'code': project.code,
            'id': project.id,
            'consultant': project.consultant if project.consultant else 'No consultant',
            'location': project.location if project.location else 'No location',
        }
        for project in projects
    ]
    return JsonResponse(project_list, safe=False)

def order_review(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    products = order.products.all()
    return render(request, 'orders/order_review.html', {'order': order, 'products': products})

@login_required
def order_form(request, order_id=None):
    order = Order.objects.get(id=order_id) if order_id else None
    context = {
        'order': order,
        'requester_username': request.user.username  # Pass the current user's username to the template
    }
    return render(request, 'orders/order_form.html', context)

def delete_order(request, order_id):
    Order.objects.filter(id=order_id).delete()
    return redirect('order_list')

def project_search_view(request):
    # منطق البحث عن المشروع
    data = {}  # تعريف المتغ data كقاموس فارغ
    # يمكنك إضافة بيانات إلى القاموس هنا بناءً على منطق البحث
    return JsonResponse(data)