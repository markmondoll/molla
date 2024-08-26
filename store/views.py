from django.shortcuts import render
from django.views.generic import ListView, DetailView

# product models
from store.models import Category, Product

class HomeListView(ListView):
    model = Product
    template_name = 'store/index.html'
    context_object_name = 'products'
    