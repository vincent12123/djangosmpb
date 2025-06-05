from django import forms
from .models import Siswa, OrangTua, Wali, SekolahAsal, JalurPendaftaran, Domisili, BantuanSosial, Dokumen

class SiswaForm(forms.ModelForm):
    class Meta:
        model = Siswa
        exclude = ['user', 'created_at', 'updated_at', 'status_pendaftaran']
        widgets = {
            'tanggal_lahir': forms.DateInput(attrs={'type': 'date'}),
        }

class OrangTuaForm(forms.ModelForm):
    class Meta:
        model = OrangTua
        exclude = ['siswa', 'created_at', 'updated_at']

class WaliForm(forms.ModelForm):
    class Meta:
        model = Wali
        exclude = ['siswa', 'created_at', 'updated_at']

class SekolahAsalForm(forms.ModelForm):
    class Meta:
        model = SekolahAsal
        exclude = ['siswa', 'created_at', 'updated_at']

class JalurPendaftaranForm(forms.ModelForm):
    class Meta:
        model = JalurPendaftaran
        exclude = ['siswa', 'created_at', 'updated_at']

class DomisiliForm(forms.ModelForm):
    class Meta:
        model = Domisili
        exclude = ['siswa', 'created_at', 'updated_at']

class BantuanSosialForm(forms.ModelForm):
    class Meta:
        model = BantuanSosial
        exclude = ['siswa', 'created_at', 'updated_at']

class DokumenForm(forms.ModelForm):
    class Meta:
        model = Dokumen
        exclude = ['siswa', 'created_at', 'updated_at']
