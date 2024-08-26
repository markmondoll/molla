from django.shortcuts import render, redirect
from django.http import HttpResponse

from profiles.forms import RegistrationForm

# Authentication Function
from django.contrib.auth import login, logout, authenticate

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
        return HttpResponse('You are logged in!')
    else:
        if request.method == 'post' or request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            customer = authenticate(request, username=username, password=password)
            if customer is not None:
                login(request, customer)
                return HttpResponse('You are logged in successfully!')
            else:
                return HttpResponse('404')
            
    return render(request, 'account/login.html')