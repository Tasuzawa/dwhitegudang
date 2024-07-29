from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Produk)
admin.site.register(Kategori)
admin.site.register(Brand)
admin.site.register(Gudang)
admin.site.register(Staff)
admin.site.register(AksesStaf)
admin.site.register(Inventory)
admin.site.register(Stok)
admin.site.register(AktivitasGudang)
admin.site.register(OnlineShop)
admin.site.register(TokoOnlineShop)
admin.site.register(LokasiToko)
admin.site.register(Order)
admin.site.register(OrderItem)