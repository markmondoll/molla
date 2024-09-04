from typing import Any
from django.shortcuts import render
from django.views.generic import ListView, DetailView

# product models
from store.models import Category, Product, ProductImages

class HomeListView(ListView):
    model = Product
    template_name = 'store/index.html' 
    context_object_name = 'products'
    
# Class Based View
class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_images'] = ProductImages.objects.filter(product=self.object.id)
        return context


# Function based view for item.get_product_url

# def product_details(request, pk):
#     item = Product.objects.get(id=pk)
#     photos = ProductImages.objects.filter(product=item).order_by('-created')
#     context = { 
#         'item': item
#         'photos': photos
#     }
#     return render(request, 'store/product.html', context)