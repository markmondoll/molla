from django.shortcuts import render
from django.views.generic import ListView, DetailView


def Home(request):
    return render(request, 'product/index.html')