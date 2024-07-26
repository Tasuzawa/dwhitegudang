# Generated by Django 4.2 on 2024-07-26 13:11

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_alter_produk_gambar'),
    ]

    operations = [
        migrations.CreateModel(
            name='AksesStaf',
            fields=[
                ('akses_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('dapat_akses', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Gudang',
            fields=[
                ('gudang_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nama_gudang', models.CharField(max_length=255)),
                ('alamat', models.TextField()),
                ('lokasi', models.CharField(max_length=255)),
                ('jenis', models.CharField(choices=[('pusat', 'Gudang Pusat'), ('cabang', 'Gudang Cabang')], max_length=255)),
                ('tanggal_dibuat', models.DateTimeField(auto_now_add=True)),
                ('gudang_pusat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.gudang')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('staff_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('foto_profile', models.ImageField(upload_to=core.models.staf_image_path)),
                ('nama_staff', models.CharField(max_length=255)),
                ('nomor_telepon', models.CharField(max_length=20)),
                ('tanggal_masuk', models.DateField()),
                ('gudang', models.ManyToManyField(through='core.AksesStaf', to='core.gudang')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='aksesstaf',
            name='gudang',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.gudang'),
        ),
        migrations.AddField(
            model_name='aksesstaf',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.staff'),
        ),
    ]
