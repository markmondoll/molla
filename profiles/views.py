from django.shortcuts import render, redirect
from django.http import HttpResponse

from profiles.forms import RegistrationForm, ProfileForm

# Authentication Function
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

from order.models import Cart, Order
from payment.models import BillingAddress
from payment.forms import BillingAddressForm
from profiles.models import Profile

from django.views.generic import TemplateView
# logout view
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

# Writing Fies as Function View
def Register(request):
    if request.user.is_authenticated:
        return HttpResponse('You are authenticated')
    else:
        form = RegistrationForm()
        if request.method == 'post' or request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse('Your account has been created')
    context = {
        'form': form
    }
    return render(request, 'account/register.html', context)

def CustomerLogin(request):
    if request.user.is_authenticated:
        return redirect('store:index')
    else:
        if request.method == 'POST' or request.method == 'post':
            username = request.POST.get('username')
            password = request.POST.get('password')
            customer = authenticate(request, username=username, password=password)
            if customer is not None:
                login(request, customer)
                return redirect('store:index')
            else:
                return HttpResponse('404')
            
    return render(request, 'account/login.html')

def CustomerLogout(request):
    logout(request)
    return redirect('profiles:login')

# Customers profile
class ProfileView(TemplateView):
    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user=request.user, ordered=True)
        billing_address = BillingAddress.objects.get(user=request.user)
        billing_address_form = BillingAddressForm(instance=billing_address)

        profile_obj = Profile.objects.get(user=request.user)
        profile_form = ProfileForm(instance=profile_obj)

        context = {
            'orders': orders,
            'billing_address': billing_address_form,
            'profile_form': profile_form,
        }
        return render(request, 'account/profile.html', context)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST' or request.method =='post':
            billing_address = BillingAddress.objects.get(user=request.user)
            billing_address_form = BillingAddressForm(request.POST, instance=billing_address)
            profile_obj = Profile.objects.get(user=request.user)
            profile_form = ProfileForm(request.POST, instance=profile_obj)
            if billing_address_form.is_valid() or profile_form.is_valid:
                billing_address_form.save()
                profile_form.save()
                return redirect('profiles:profile')


