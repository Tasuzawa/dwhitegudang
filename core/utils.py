from django.utils.text import slugify
from django.db.models import Sum
# Models
from core.models import *


def update_user_permission_bygrup(sender, instance, created, **kwargs):
    """
    Memperbarui izin pengguna berdasarkan jabatannya.

    Signal ini akan dijalankan ketika pengguna baru dibuat atau ketika field jabatan
    pada model Staff diubah.
    """
    if created or hasattr(instance, 'staff') and instance.staff.jabatan:
        jabatan = instance.staff.jabatan
        if jabatan:
            # Hapus semua grup yang sudah ada
            instance.groups.clear()
            # Tambahkan grup baru berdasarkan jabatan
            instance.groups.add(jabatan.grup_auth)
            instance.save()

def update_order_total_qty(sender, instance, created, **kwargs):
    order = instance.order
    order.total_qty = order.orderitem_set.aggregate(total_qty=Sum('qty'))['total_qty'] or 0
    order.save()
    

def update_stok_aktual_inventory(sender, instance, created, **kwargs):
    if created:
        stok = instance.stok
        if instance.jenis_aktivitas == 'masuk':
            stok.stok_aktual += instance.jumlah
        elif instance.jenis_aktivitas == 'keluar':
            stok.stok_aktual -= instance.jumlah
        elif instance.jenis_aktivitas == 'sesuaikan':
            stok.stok_aktual = instance.jumlah
        stok.save()

        

def produk_image_path(instance, filename):
    nama_file = slugify(instance.nama_produk)
    ext = filename.split('.')[-1]
    filename = f'{nama_file}.{ext}'
    
    return f'produk/{instance.produk_id}/{filename}'
        

def staf_image_path(instance, filename):
    nama_file = slugify(instance.nama_staff)
    ext = filename.split('.')[-1]
    filename = f'{nama_file}.{ext}'
    
    return f'staf/foto_profile/{instance.staff_id}/{filename}'


def order_resi_pdf_path(instance, filename):
    nama_file = slugify(instance.nomor_resi)
    ext = filename.split('.')[-1]
    filename = f'{nama_file}.{ext}'
    
    return f'order/{instance.order_id}/resi/{filename}'