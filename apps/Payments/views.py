# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Payment
from .forms import PaymentForm

# List view for payments
def payment_list(request):
    payments = Payment.objects.all()
    return render(request, 'payment_list.html', {'payments': payments})

# Create view for payment
def payment_create(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payment/payment_list')
    else:
        form = PaymentForm()
    return render(request, 'payment/payment_form.html', {'form': form})

# Update view for payment
def payment_update(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return redirect('payment/payment_list')
    else:
        form = PaymentForm(instance=payment)
    return render(request, 'payment/payment_form.html', {'form': form})

# Delete view for payment
def payment_delete(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        payment.delete()
        return redirect('payment/payment_list')
    return render(request, 'payment/payment_confirm_delete.html', {'payment': payment})

# Detail view for payment
def payment_detail(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    return render(request, 'payment/payment_detail.html', {'payment': payment})
