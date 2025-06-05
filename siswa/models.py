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
    jenis_kelamin = models.CharField(max_length=10, choices=[('Laki-laki', 'Laki-laki'), ('Perempuan', 'Perempuan')])
    agama = models.CharField(max_length=20, choices=[
        ('Islam', 'Islam'),
        ('Kristen', 'Kristen'),
        ('Katolik', 'Katolik'),
        ('Hindu', 'Hindu'),
        ('Buddha', 'Buddha'),
        ('Konghucu', 'Konghucu'),
        ('Lainnya', 'Lainnya')
    ])
    kewarganegaraan = models.CharField(max_length=50, default='Indonesia')
    berkebutuhan_khusus = models.CharField(max_length=50, choices=[
        ('Tidak Ada', 'Tidak Ada'),
        ('Tunanetra', 'Tunanetra'),
        ('Tunarungu', 'Tunarungu'),
        ('Tunadaksa', 'Tunadaksa'),
        ('Tunagrahita', 'Tunagrahita'),
        ('Lainnya', 'Lainnya')
    ], default='Tidak Ada')
    alamat = models.TextField()
    telepon = models.CharField(max_length=15)
    telepon_rumah = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    status_pendaftaran = models.CharField(max_length=20, default='draft')
    # Data kesehatan
    tinggi_badan = models.PositiveIntegerField(blank=True, null=True)
    berat_badan = models.PositiveIntegerField(blank=True, null=True)
    lingkar_kepala = models.PositiveIntegerField(blank=True, null=True)
    golongan_darah = models.CharField(max_length=3, blank=True, null=True)
    riwayat_penyakit = models.TextField(blank=True, null=True)
    kelainan_jasmani = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nama_lengkap} ({self.nisn})"

class OrangTua(models.Model):
    siswa = models.OneToOneField(Siswa, on_delete=models.CASCADE, related_name='orang_tua')
    # Data Ayah
    nama_ayah = models.CharField(max_length=100)
    nik_ayah = models.CharField(max_length=16, blank=True, null=True)
    pendidikan_ayah = models.CharField(max_length=20, blank=True, null=True)
    pekerjaan_ayah = models.CharField(max_length=50)
    penghasilan_ayah = models.CharField(max_length=50, blank=True, null=True)
    telepon_ayah = models.CharField(max_length=15, blank=True, null=True)
    # Data Ibu
    nama_ibu = models.CharField(max_length=100)
    nik_ibu = models.CharField(max_length=16, blank=True, null=True)
    pendidikan_ibu = models.CharField(max_length=20, blank=True, null=True)
    pekerjaan_ibu = models.CharField(max_length=50)
    penghasilan_ibu = models.CharField(max_length=50, blank=True, null=True)
    telepon_ibu = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Orang Tua {self.siswa.nama_lengkap}"

class Wali(models.Model):
    siswa = models.OneToOneField(Siswa, on_delete=models.CASCADE, related_name='wali', blank=True, null=True)
    nama_wali = models.CharField(max_length=100, blank=True, null=True)
    nik_wali = models.CharField(max_length=16, blank=True, null=True)
    pendidikan_wali = models.CharField(max_length=20, blank=True, null=True)
    pekerjaan_wali = models.CharField(max_length=50, blank=True, null=True)
    penghasilan_wali = models.CharField(max_length=50, blank=True, null=True)
    telepon_wali = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Wali {self.siswa.nama_lengkap}"

class SekolahAsal(models.Model):
    siswa = models.OneToOneField(Siswa, on_delete=models.CASCADE, related_name='sekolah_asal')
    nama_sekolah = models.CharField(max_length=100)
    npsn = models.CharField(max_length=8, blank=True, null=True)
    alamat_sekolah = models.TextField()
    tahun_lulus = models.IntegerField()
    rata_nilai_rapor = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.nama_sekolah} ({self.siswa.nama_lengkap})"

class JalurPendaftaran(models.Model):
    JALUR_CHOICES = [
        ('domisili', 'Jalur Domisili'),
        ('afirmasi', 'Jalur Afirmasi'),
        ('prestasi', 'Jalur Prestasi'),
        ('mutasi', 'Jalur Mutasi')
    ]
    siswa = models.OneToOneField(Siswa, on_delete=models.CASCADE, related_name='jalur_pendaftaran')
    jalur = models.CharField(max_length=20, choices=JALUR_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.get_jalur_display()} - {self.siswa.nama_lengkap}"

class Domisili(models.Model):
    siswa = models.OneToOneField(Siswa, on_delete=models.CASCADE, related_name='domisili')
    jarak_rumah_sekolah = models.DecimalField(max_digits=5, decimal_places=2)
    waktu_tempuh = models.IntegerField(help_text="Waktu tempuh dalam menit")
    moda_transportasi = models.CharField(max_length=50)
    lama_tinggal_kk = models.IntegerField(help_text="Lama tinggal dalam tahun")
    dokumen_kk = models.CharField(max_length=200, blank=True, null=True)
    dokumen_ktp = models.CharField(max_length=200, blank=True, null=True)
    dokumen_surat_domisili = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Domisili {self.siswa.nama_lengkap}"

class BantuanSosial(models.Model):
    siswa = models.OneToOneField(Siswa, on_delete=models.CASCADE, related_name='bantuan_sosial')
    kip_status = models.BooleanField(default=False)
    kip_nomor = models.CharField(max_length=50, blank=True, null=True)
    pkh_status = models.BooleanField(default=False)
    pkh_nomor = models.CharField(max_length=50, blank=True, null=True)
    kps_status = models.BooleanField(default=False)
    kps_nomor = models.CharField(max_length=50, blank=True, null=True)
    status_disabilitas = models.CharField(max_length=50, blank=True, null=True)
    dokumen_kip_pkh = models.CharField(max_length=200, blank=True, null=True)
    dokumen_tidak_mampu = models.CharField(max_length=200, blank=True, null=True)
    dokumen_disabilitas = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Bantuan Sosial {self.siswa.nama_lengkap}"

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
