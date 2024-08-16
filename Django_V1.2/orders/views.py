from django.shortcuts import render, redirect, get_object_or_404
from .models import Order
from products.models import Product
from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
import datetime
from django.utils import timezone
from django.http import JsonResponse
from django.http import Http404
from django.contrib import messages

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['product_name', 'product_code', 'quantity', 'supply_date', 'request_date', 'project_name', 'project_code', 'order_name', 'project_phase', 'project_consultant', 'project_location']
        widgets = {
            'supply_date': forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date().isoformat()}),
            'request_date': forms.DateInput(attrs={'type': 'date', 'readonly': 'readonly', 'value': timezone.now().date().isoformat()}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_name'].widget.attrs.update({'class': 'autocomplete'})
        self.fields['product_code'].widget.attrs.update({'class': 'autocomplete'})

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

    def clean_supply_date(self):
        supply_date = self.cleaned_data.get('supply_date')
        today = timezone.now().date()
        if supply_date and supply_date < today:
            raise ValidationError("Supply date cannot be in the past.")
        return supply_date
    
    def clean_request_date(self):
        request_date = self.cleaned_data.get('request_date')
        today = timezone.now().date()
        if request_date and request_date != today:
            raise ValidationError("Request date must be today.")
        return request_date
    
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
    
def order_list(request):
    orders = Order.objects.all().order_by('-order_date')
    print(f"Total orders in database: {Order.objects.count()}")
    print(f"Orders being sent to template: {len(orders)}")
    return render(request, 'orders/orders_list.html', {'orders': orders})

def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.request_date = timezone.now().date()  # Ensure request_date is always today
            product_name = form.cleaned_data['product_name']
            product_code = form.cleaned_data['product_code']
            try:
                product = Product.objects.get(name=product_name, code=product_code)
                if order.quantity <= product.stock:
                    product.stock -= order.quantity
                    product.save()
                    order.save()
                    return redirect('order_list')
                else:
                    form.add_error('quantity', f"Only {product.stock} available. Cannot order more than that.")
            except Product.DoesNotExist:
                form.add_error(None, "Product not found. Please enter a valid product name and code.")
    else:
        form = OrderForm(initial={'supply_date': timezone.now().date(), 'request_date': timezone.now().date()})
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

def order_delete(request, id):
    order = get_object_or_404(Order, id=id)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'orders/orders_confirm_delete.html', {'object': order})

def order_approve(request, id):
    order = get_object_or_404(Order, id=id)
    order.status = 'approved'
    order.approved_by = request.POST.get('approved_by', 'Unknown')
    order.save()
    messages.success(request, f'Approved by {request.user.username}')
    return redirect('order_detail', id=id)  # Redirect to the detail page

def order_disapprove(request, id):
    order = get_object_or_404(Order, id=id)
    order.status = 'disapproved'
    order.disapproved_by = request.POST.get('disapproved_by', 'Unknown')
    order.save()
    messages.error(request, f'Disapproved by {request.user.username}')
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

# def submit_order(request):
#     if request.method == 'POST':
#         # استخراج البيانات من النموذج
#         order_data = {
#             'request_date': request.POST.get('request_date'),
#             'supply_date': request.POST.get('supply_date'),
#             'order_name': request.POST.get('order_name'),
#             'project_name': request.POST.get('project_name'),
#             'project_code': request.POST.get('project_code'),
#             'project_consultant': request.POST.get('project_consultant'),
#             'project_location': request.POST.get('project_location'),
#             'project_phase': request.POST.get('project_phase'),
#             'products': [
#                 {
#                     'name': name,
#                     'code': code,
#                     'quantity': quantity
#                 }
#                 for name, code, quantity in zip(
#                     request.POST.getlist('product_name[]'),
#                     request.POST.getlist('product_code[]'),
#                     request.POST.getlist('quantity[]')
#                 )
#             ]
#         }
#         # إرسال البيانات إلى صفحة الملخص
#         return render(request, 'orders/summary.html', {'order': order_data})
#     return redirect('order_form')

# def order_summary(request, order_id):
#     try:
#         order = Order.objects.get(id=order_id)
#         total_orders = Order.objects.count()
#         order_number = total_orders + 1
#     except Order.DoesNotExist:
#         raise Http404("Order does not exist")

#     context = {
#         'order': order,
#         'order_number': f"Order No.{order_number}"
#     }
#     return render(request, 'orders/summary.html', context)

# def add_order(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # Redirect to a new URL:
#             return redirect('order_success')
#     else:
#         form = OrderForm()

#     return render(request, 'orders/orders_form.html', {'form': form})