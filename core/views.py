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