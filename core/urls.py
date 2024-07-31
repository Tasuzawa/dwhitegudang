from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('accounts/login', views.UserLogin, name='login'),
    path('accounts/register', views.UserRegister, name='register'),
]