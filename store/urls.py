from django.urls import path
from store import views

app_name = "store"
urlpatterns = [
    path('', views.HomeListView.as_view(), name='index'),
    path('product/<slug>/', views.ProductDetailView.as_view(), name='product-details'),
    path('about/', views.about, name='about'),
    path('products/', views.ProductistView.as_view(), name='product'),
]
