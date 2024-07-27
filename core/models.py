import uuid
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

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

def generate_batch_number(sender, instance, **kwargs):
    if not instance.batch_number:
        # Ambil singkatan dari nama produk dan gudang
        singkatan_produk = instance.produk.nama_produk[:3]
        singkatan_gudang = instance.gudang.nama_gudang[:3]

        # Cari batch number terakhir dengan awalan yang sama
        last_batch = Inventory.objects.filter(
            batch_number__startswith=f"{singkatan_produk}{singkatan_gudang}"
        ).order_by('-batch_number').first()

        if last_batch:
            # Ambil nomor urut terakhir dan tambahkan 1
            last_number = int(last_batch.batch_number[-3:]) + 1
        else:
            last_number = 1

        # Format batch number baru
        instance.batch_number = f"{singkatan_produk}{singkatan_gudang}{str(last_number).zfill(3)}"





class Inventory(models.Model):
  inventory_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  gudang = models.ForeignKey(Gudang, on_delete=models.CASCADE)
  produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
  satuan = models.CharField(max_length=20, choices=[
      ('pcs', 'Pieces'),
      ('paket', 'Paket'),
  ])
  level_stok = models.PositiveIntegerField(default=0)
  level_minimum = models.PositiveIntegerField(default=0)
  stok_aktual = models.PositiveIntegerField(default=0)
  batch_number = models.CharField(max_length=50, null=True, blank=True, editable=False)
  lokasi_rak = models.CharField(max_length=100, null=True, blank=True)
  
  def __str__(self):
      return f'{self.produk.nama_produk} - {self.gudang.nama_gudang}'
  
# Hubungkan fungsi dengan sinyal pre_save
pre_save.connect(generate_batch_number, sender=Inventory)

class Stok(models.Model):
    stok_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    gudang = models.ForeignKey(Gudang, on_delete=models.CASCADE)
    jumlah = models.PositiveIntegerField(default=0)
    tanggal_masuk = models.DateTimeField(auto_now_add=True)
    tanggal_kadaluarsa = models.DateField(null=True, blank=True)
    lokasi_rak = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.inventory
    
    
class AktivitasGudang(models.Model):
    aktivitas_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stok = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    jenis_aktivitas = models.CharField(max_length=20, choices=[
        ('masuk', 'Barang Masuk'),
        ('keluar', 'Barang Keluar'),
        ('sesuaikan', 'Penyesuaian Stok'),
    ])
    jumlah = models.PositiveIntegerField()
    tanggal_aktivitas = models.DateTimeField(auto_now_add=True)
    nama_staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)  # Hubungan dengan model User
    keterangan = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.tanggal_aktivitas}-{self.jenis_aktivitas}-{self.jumlah}-{self.stok}'
    


def update_stok_aktual(sender, instance, created, **kwargs):
    if created:
        stok = instance.stok
        if instance.jenis_aktivitas == 'masuk':
            stok.stok_aktual += instance.jumlah
        elif instance.jenis_aktivitas == 'keluar':
            stok.stok_aktual -= instance.jumlah
        elif instance.jenis_aktivitas == 'sesuaikan':
            stok.stok_aktual = instance.jumlah
        stok.save()

# Hubungkan fungsi dengan sinyal post_save
post_save.connect(update_stok_aktual, sender=AktivitasGudang)