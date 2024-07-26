import uuid
from django.db import models
from django.utils.text import slugify

# Create your models here.
class Kategori(models.Model):
    kategori_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_kategori = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nama_kategori
    
class Brand(models.Model):
    brand_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_brand = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nama_brand


def produk_image_path(instance, filename):
    nama_file = slugify(instance.nama_produk)
    ext = filename.split('.')[-1]
    filename = f'{nama_file}.{ext}'
    return f'media/produk_gambar/{instance.produk_id}/{filename}'


class Produk(models.Model):
    produk_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_produk = models.CharField(max_length=500)
    deskripsi = models.TextField()
    harga_hpp = models.DecimalField(max_digits=10, decimal_places=0)
    harga_jual = models.DecimalField(max_digits=10, decimal_places=0)
    kategori = models.ForeignKey('Kategori', on_delete=models.CASCADE)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)
    tanggal_diperbarui = models.DateTimeField(auto_now=True)
    gambar = models.ImageField(upload_to=produk_image_path)
    
    def __str__(self):
        return self.nama_produk
    