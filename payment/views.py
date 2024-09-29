from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

# View
from django.views.generic import TemplateView

#  Models
from payment.models import BillingAddress
from payment.forms import BillingAddressForm, PaymentMethodForm
from order.models import Cart, Order

# PayPal
from django.conf import settings
import json

# SSLcommerz
from sslcommerz_python.payment import SSLCSession

from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal

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
            'paypal_client_id': settings.PAYPAL_CLIENT_ID
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
                    order.payment_id = order.id
                    order.save()
                    cart_items = Cart.objects.filter(user=request.user, purchased=False)
                    for item in cart_items:
                        item.purchased = True
                        item.save()
                    print('Order Submitted Successfully')
                    return redirect('store:index')
                
                # PayPal payment process
                #if pay_method.payment_method =='PayPal':
                    #return redirect(reverse('payment:checkout') + "?pay_meth=" +str(pay_method.payment_method))
                
                # SSLcommerz payment process
                if pay_method.payment_method == 'SSLcommerz':
                    store_id = settings.STORE_ID
                    store_pass = settings.STORE_PASS
                    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=store_pass)

                    status_url = request.build_absolute_uri(reverse('payment:status'))
                    mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)

                    order_qs = Order.objects.filter(user=request.user, ordered=False)
                    order_items = order_qs[0].order_items.all()
                    order_item_count = order_qs[0].order_items.count()
                    order_total = order_qs[0].get_totals()
                    mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT', product_category='clothing', product_name=order_items, num_of_item=order_item_count, shipping_method='Courier', product_profile='None')

                    current_user = request.user
                    mypayment.set_customer_info(name=current_user.profile.full_name, email=current_user.email, address1=current_user.profile.address, address2=current_user.profile.address, city=current_user.profile.city, postcode=current_user.profile.zip_code, country=current_user.profile.country, phone=current_user.profile.phone)
                    mypayment.set_shipping_info(shipping_to=current_user.profile.full_name, address=current_user.profile.address, city=current_user.profile.city, postcode=current_user.profile.zip_code, country=current_user.profile.country)

                    response_data = mypayment.init_payment()
                    print('==============================================================')
                    print(response_data)
                    return redirect(response_data['GatewayPageURL'])
                    print('==================================================================')
                return redirect('payment:checkout')


@csrf_exempt
def sslc_status(request):
    if request.method == 'post' or request.method == 'POST':
        payment_data = request.POST
        status = payment_data['status']
        if status == 'VALID':
            val_id = payment_data['val_id']
            tran_id = payment_data['tran_id']
            return HttpResponseRedirect(reverse('payment:sslc_complete', kwargs={'val_id': val_id, 'tran_id': tran_id}))

    return render(request, 'store/status.html')

def sslc_complete(request, val_id, tran_id):
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs[0]
    order.ordered = True
    order.order_id = val_id
    order.payment_id = tran_id
    order.payment_method = 'SSLcommerz'
    order.save()
    cart_items = Cart.objects.filter(user=request.user, purchased=False)
    for item in cart_items:
        item.purchased = True
        item.save()
    
    return redirect('store:index')

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
            order.payment_method = 'PayPal'
            order.save()
            cart_items = Cart.objects.filter(user=request.user, purchased=False)
            for item in cart_items:
                item.purchased = True
                item.save()
    return redirect('store:index')
