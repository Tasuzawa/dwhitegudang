import uuid
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# function Models
from  core.utils import *

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

class Jabatan(models.Model):
    jabatan_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_jabatan = models.CharField(max_length=255)
    grup_auth = models.ForeignKey(Group, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nama_jabatan

    
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    foto_profile = models.ImageField(upload_to=staf_image_path)
    nama_staff = models.CharField(max_length=255)
    nomor_telepon = models.CharField(max_length=20)
    tanggal_masuk = models.DateField()
    jabatan = models.ForeignKey('Jabatan', on_delete=models.CASCADE)
    gudang = models.ManyToManyField(Gudang, through='AksesStaf')
    
    def __str__(self):
        return self.nama_staff
    
post_save.connect(update_user_permission_bygrup, sender=Staff)
    
        
    
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
        sort_produk = instance.produk.nama_produk[:3]
        sort_gudang = instance.gudang.nama_gudang[:3]
        
        last_batch = Inventory.objects.filter(
            batch_number__startswith=f"{sort_produk}{sort_gudang}"
        ).order_by('-batch_number').first()
        
        if last_batch:
            last_number = int(last_batch.batch_number[-3:]) + 1
            
        else:
            last_number = 1
        
        instance.batch_number = f"{sort_produk}{sort_gudang}{str(last_number).zfill(3)}"


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
    
  
# fungsi untuk mengatur batch_number secara automatis sebelum menyimpan ke database
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
        return f'{self.inventory}'
    
    
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
    
# fungsi untuk mengatur stok secara automatis setelah menyimpan ke database
post_save.connect(update_stok_aktual_inventory, sender=AktivitasGudang)

class OnlineShop(models.Model):
    online_shop_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_online_shop = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nama_online_shop
    
class TokoOnlineShop(models.Model):
    toko_online_shop_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    online_shop = models.ForeignKey(OnlineShop, on_delete=models.CASCADE)
    id_toko = models.CharField(max_length=255)
    nama_toko = models.CharField(max_length=255)
    alamat = models.TextField()
    nomor_telepon = models.CharField(max_length=20)
    penanggung_jawab = models.CharField(max_length=255)
    
    def __str__(self):
        return f'{self.online_shop}-{self.nama_toko}'
    
class LokasiToko(models.Model):
    lokasi_toko_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    toko_online_shop = models.ForeignKey(TokoOnlineShop, on_delete=models.CASCADE)
    gudang = models.ForeignKey(Gudang, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.toko_online_shop} - {self.gudang}'

    
    
class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lokasi_kirim = models.ForeignKey(Gudang, on_delete=models.CASCADE) 
    toko = models.ForeignKey(LokasiToko, on_delete=models.CASCADE)
    nomor_resi = models.CharField(max_length=255)
    nama_customer = models.CharField(max_length=255)
    nomor_telepon = models.CharField(max_length=20)
    alamat = models.TextField()
    kota_kecamatan = models.CharField(max_length=500)
    metode_pembayaran = models.CharField(max_length=255, choices=[
        ('cod', 'Cash On Delivery'),
        ('transfer', 'Transfer Bank'),
    ])
    produk = models.ManyToManyField(Inventory, through='OrderItem')
    total_qty = models.PositiveIntegerField(editable=False, default=0)
    total_pembayaran = models.DecimalField(max_digits=10, decimal_places=0)
    ongkos_kirim = models.DecimalField(max_digits=10, decimal_places=0)
    tanggal_order = models.DateTimeField(auto_now_add=True, editable=False)
    tanggal_selesai = models.DateTimeField(null=True, blank=True, editable=False)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('proses', 'Proses'),
        ('siap', 'Siap Kirim'),
        ('dikirim', 'Sudah Dikirim'),
        ('selesai', 'Selesai'),
        ('dibatalkan', 'Dibatalkan'),
        ('retur','retur'),
    ], default='pending', editable=False)
    resi = models.FileField(upload_to=order_resi_pdf_path)
    
    
    def __str__(self):
        return f'{self.nama_customer} - {self.toko}'
    

class OrderItem(models.Model):
    order_item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    produk = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    
    def __str__(self):
        return f'{self.order}-{self.produk.produk}-{self.qty}'

   
post_save.connect(update_order_total_qty, sender=OrderItem)


class Pelanggan(models.Model):
    pelanggan_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = models.CharField(max_length=255)
    nomor_telepon = models.CharField(max_length=20)
    alamat = models.TextField()
    pesanan = models.ManyToManyField(Order)

    def __str__(self):
        return self.nama

def create_or_update_pelanggan(sender, instance, created, **kwargs):
    if created:
        pelanggan, created = Pelanggan.objects.get_or_create(
            nama=instance.nama_customer,
            nomor_telepon=instance.nomor_telepon,
            defaults={
                'alamat': instance.alamat,
            }
        )
        instance.pelanggan = pelanggan
        instance.save()
        
        pelanggan.pesanan.add(instance)

post_save.connect(create_or_update_pelanggan, sender=Order)