from django.db import models
from django.conf import settings
from django.utils import timezone

class Siswa(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='siswa')
    nama_lengkap = models.CharField(max_length=100)
    nisn = models.CharField(max_length=20, unique=True)
    nik = models.CharField(max_length=20, unique=True)
    tempat_lahir = models.CharField(max_length=50)
    tanggal_lahir = models.DateField()
    jenis_kelamin = models.CharField(max_length=10)
    agama = models.CharField(max_length=20)
    alamat = models.TextField()
    telepon = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    status_pendaftaran = models.CharField(max_length=20, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nama_lengkap} ({self.nisn})"

class OrangTua(models.Model):
    siswa = models.OneToOneField(Siswa, on_delete=models.CASCADE, related_name='orang_tua')
    nama_ayah = models.CharField(max_length=100)
    nama_ibu = models.CharField(max_length=100)
    pekerjaan_ayah = models.CharField(max_length=50)
    pekerjaan_ibu = models.CharField(max_length=50)
    telepon_ayah = models.CharField(max_length=15)
    telepon_ibu = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Orang Tua {self.siswa.nama_lengkap}"

class SekolahAsal(models.Model):
    siswa = models.OneToOneField(Siswa, on_delete=models.CASCADE, related_name='sekolah_asal')
    nama_sekolah = models.CharField(max_length=100)
    alamat_sekolah = models.TextField()
    tahun_lulus = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nama_sekolah} ({self.siswa.nama_lengkap})"

class Dokumen(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE, related_name='dokumen')
    jenis_dokumen = models.CharField(max_length=50)
    file_path = models.CharField(max_length=200)
    status = models.CharField(max_length=20, default='Diupload')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.jenis_dokumen} - {self.siswa.nama_lengkap}"

class Verifikasi(models.Model):
    siswa = models.OneToOneField(Siswa, on_delete=models.CASCADE, related_name='verifikasi')
    status = models.CharField(max_length=20, default='Menunggu')
    catatan = models.TextField(blank=True, null=True)
    tanggal_verifikasi = models.DateTimeField(default=timezone.now)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='verifikasi_admin')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Verifikasi {self.siswa.nama_lengkap} - {self.status}"

class Soal(models.Model):
    pertanyaan = models.TextField()
    tipe = models.CharField(max_length=20, default='pilihan_ganda')
    pilihan_a = models.CharField(max_length=255, blank=True, null=True)
    pilihan_b = models.CharField(max_length=255, blank=True, null=True)
    pilihan_c = models.CharField(max_length=255, blank=True, null=True)
    pilihan_d = models.CharField(max_length=255, blank=True, null=True)
    pilihan_e = models.CharField(max_length=255, blank=True, null=True)
    jawaban_benar = models.CharField(max_length=10)
    aktif = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Soal #{self.id} - {self.pertanyaan[:30]}..."

class JawabanSiswa(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE, related_name='jawaban_soal')
    soal = models.ForeignKey(Soal, on_delete=models.CASCADE, related_name='jawaban_siswa')
    jawaban = models.CharField(max_length=255)
    benar = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Jawaban {self.siswa.nama_lengkap} untuk Soal #{self.soal.id}"
