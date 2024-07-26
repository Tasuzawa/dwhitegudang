import uuid
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

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
    return f'produk_gambar/{instance.produk_id}/{filename}'


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


class Gudang(models.Model):
    gudang_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_gudang = models.CharField(max_length=255)
    alamat = models.TextField()
    lokasi = models.CharField(max_length=255)
    jenis = models.CharField(max_length=255, choices=[
        ('pusat', 'Gudang Pusat'),
        ('cabang', 'Gudang Cabang'),
    ])
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)
    gudang_pusat = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.nama_gudang


def staf_image_path(instance, filename):
    nama_file = slugify(instance.nama_staff)
    ext = filename.split('.')[-1]
    filename = f'{nama_file}.{ext}'
    return f'staf_gambar/foto_profile/{instance.staff_id}/{filename}'

    
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    foto_profile = models.ImageField(upload_to=staf_image_path)
    nama_staff = models.CharField(max_length=255)
    nomor_telepon = models.CharField(max_length=20)
    tanggal_masuk = models.DateField()
    gudang = models.ManyToManyField(Gudang, through='AksesStaf')
    
    def __str__(self):
        return self.nama_staff
    
    
# Suggested code may be subject to a license. Learn more: ~LicenseLog:3579031129.
class AksesStaf(models.Model):
    akses_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    gudang = models.ForeignKey(Gudang, on_delete=models.CASCADE)
    dapat_akses = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.staff.nama_staff} - {self.gudang.nama_gudang}'