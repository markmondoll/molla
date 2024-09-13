from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

# Models

from payment.models import BillingAddress
from payment.forms import BillingAddressForm, PaymentMethodForm
from order.models import Cart, Order

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
            'payment_method': payment_method
        }
        return render(request, 'payment/checkout.html', context)

    def post(self, reqest, *args, **kwargs):
        pass