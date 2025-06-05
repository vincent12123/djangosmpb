from django.contrib import admin
from .models import Siswa, OrangTua, SekolahAsal, Dokumen, Verifikasi, Soal, JawabanSiswa

class OrangTuaInline(admin.StackedInline):
    model = OrangTua
    can_delete = False
    extra = 0

class SekolahAsalInline(admin.StackedInline):
    model = SekolahAsal
    can_delete = False
    extra = 0

class DokumenInline(admin.TabularInline):
    model = Dokumen
    extra = 0

class VerifikasiInline(admin.StackedInline):
    model = Verifikasi
    can_delete = False
    extra = 0

@admin.register(Siswa)
class SiswaAdmin(admin.ModelAdmin):
    list_display = ('nama_lengkap', 'nisn', 'nik', 'status_pendaftaran', 'email', 'created_at')
    list_filter = ('status_pendaftaran', 'jenis_kelamin', 'agama')
    search_fields = ('nama_lengkap', 'nisn', 'nik', 'email')
    inlines = [OrangTuaInline, SekolahAsalInline, DokumenInline, VerifikasiInline]
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Verifikasi)
class VerifikasiAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'status', 'tanggal_verifikasi', 'admin')
    list_filter = ('status',)
    search_fields = ('siswa__nama_lengkap',)
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(OrangTua)
admin.site.register(SekolahAsal)
admin.site.register(Dokumen)
admin.site.register(Soal)
admin.site.register(JawabanSiswa)
