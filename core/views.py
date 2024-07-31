from django.shortcuts import render,get_object_or_404

# Database
from .models import *

# Create your views here.
def main(request):
    render_template = "main.html"
    produk = Produk.objects.all()
    context = {
        'produk':produk,
    }
    
    return render(request,render_template,context)


def UserLogin(request):
    render_template = "login.html"
    
    return render(request,render_template)


def UserRegister(request):
    render_template = "register.html"
    
    return render(request,render_template)