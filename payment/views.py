from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect


#  Models
from payment.models import BillingAddress
from payment.forms import BillingAddressForm, PaymentMethodForm
from order.models import Cart, Order

# PayPal
from django.conf import settings
import json

# View
from django.views.generic import TemplateView

class CheckoutTemplateView(TemplateView):
    def get(self, request, *args, **kwargs):
        saved_address = BillingAddress.objects.get_or_create(user=request.user or None)
        saved_address = saved_address[0]
        form = BillingAddressForm(instance=saved_address)
        payment_method = PaymentMethodForm()
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        order_item = order_qs[0].order_items.all()
        order_total = order_qs[0].get_totals()
        context = {
            'billing_address': form,
            'order_item': order_item,
            'order_total': order_total,
            'payment_method': payment_method,
            'paypal_client_id': settings.PAYPAL_CLIENT_ID,
        }
        return render(request, 'payment/checkout.html', context)

    def post(self, request, *args, **kwargs):
        saved_address = BillingAddress.objects.get_or_create(user=request.user or None)
        saved_address = saved_address[0]
        form = BillingAddressForm(instance=saved_address)
        payment_obj = Order.objects.filter(user=request.user, ordered=False)[0]
        payment_form = PaymentMethodForm(instance=payment_obj)
        if request.method == 'post' or request.method == 'POST':
            form = BillingAddressForm(request.POST, instance=saved_address)
            pay_form = PaymentMethodForm(request.POST, instance=payment_obj)
            if form.is_valid() and pay_form.is_valid():
                form.save()
                pay_method = pay_form.save()

                if not saved_address.is_fully_filled():
                    return redirect('payment:checkout')
                
                # Cash on delivery payment process
                if pay_method.payment_method == 'Cash on Delivery':
                    order_qs = Order.objects.filter(user=request.user, ordered=False)
                    order = order_qs[0]
                    order.ordered = True
                    order.order_id = order.id
                    order.payment_id = pay_method.payment_method
                    order.save()
                    cart_items = Cart.objects.filter(user=request.user, purchased=False)
                    for item in cart_items:
                        item.purchased = True
                        item.save()
                    print('Order Submitted Successfully')
                    return redirect('store:index')
                
                # paypal payment process
                if pay_method.payment_method =='PayPal':
                    return redirect(reverse('payment:checkout', kwargs={'pay_meth': pay_method.payment_method}))
                    # return redirect(f"{reverse('payment:checkout')}?pay_meth={pay_method.payment_method}")
                    # return redirect(reverse('payment:checkout') )
                


def paypalPaymentMethod(request):
    data = json.loads(request.body)
    order_id = data['order_id']
    payment_id = data['payment_id']
    status = data['status']

    if status == "COMPLETED":
        if request.user.is_authenticated:
            order_qs = Order.objects.filter(user=request.user, ordered=False)
            order = order_qs[0]
            order.ordered = True
            order.order_id = order_id
            order.payment_id = payment_id
            order.save()
            cart_items = Cart.objects.filter(user=request.user, purchased=False)
            for item in cart_items:
                item.purchased = True
                item.save()
    return redirect('store:index')
