from django.urls import path
from profiles import views

app_name = "profiles"
urlpatterns = [
    path('register/', views.Register, name='register'),
    path('login/', views.CustomerLogin, name='login'),
    path('logout/', views.CustomerLogout, name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile' ),

]
