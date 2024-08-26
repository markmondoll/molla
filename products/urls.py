from django.urls import path
from products import views
from .views import *

app_name = "products"
urlpatterns = [
    path('', views.Home, name='home'),
]
