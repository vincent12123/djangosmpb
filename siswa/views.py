from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import SiswaForm, OrangTuaForm, WaliForm, SekolahAsalForm, JalurPendaftaranForm, DomisiliForm, BantuanSosialForm, DokumenForm
from .models import Siswa, OrangTua, Wali, SekolahAsal, JalurPendaftaran, Domisili, BantuanSosial, Dokumen
from django.forms import modelformset_factory
from django.contrib import messages

@login_required
def dashboard(request):
    return render(request, 'siswa/dashboard.html')

@login_required
def status(request):
    return render(request, 'siswa/status.html')

@login_required
def formulir(request):
    user = request.user
    siswa_instance = getattr(user, 'siswa', None)
    orangtua_instance = getattr(siswa_instance, 'orang_tua', None) if siswa_instance else None
    wali_instance = getattr(siswa_instance, 'wali', None) if siswa_instance else None
    sekolahasal_instance = getattr(siswa_instance, 'sekolah_asal', None) if siswa_instance else None
    jalur_instance = getattr(siswa_instance, 'jalur_pendaftaran', None) if siswa_instance else None
    domisili_instance = getattr(siswa_instance, 'domisili', None) if siswa_instance else None
    bantuansosial_instance = getattr(siswa_instance, 'bantuan_sosial', None) if siswa_instance else None

    if request.method == 'POST':
        siswa_form = SiswaForm(request.POST, instance=siswa_instance)
        orangtua_form = OrangTuaForm(request.POST, instance=orangtua_instance)
        wali_form = WaliForm(request.POST, instance=wali_instance)
        sekolahasal_form = SekolahAsalForm(request.POST, instance=sekolahasal_instance)
        jalur_form = JalurPendaftaranForm(request.POST, instance=jalur_instance)
        domisili_form = DomisiliForm(request.POST, instance=domisili_instance)
        bantuansosial_form = BantuanSosialForm(request.POST, instance=bantuansosial_instance)
        dokumen_form = DokumenForm(request.POST, request.FILES)

        forms_valid = all([
            siswa_form.is_valid(), orangtua_form.is_valid(), wali_form.is_valid(),
            sekolahasal_form.is_valid(), jalur_form.is_valid(), domisili_form.is_valid(),
            bantuansosial_form.is_valid(), dokumen_form.is_valid()
        ])
        if forms_valid:
            siswa = siswa_form.save(commit=False)
            siswa.user = user
            siswa.save()
            orangtua = orangtua_form.save(commit=False)
            orangtua.siswa = siswa
            orangtua.save()
            wali = wali_form.save(commit=False)
            wali.siswa = siswa
            wali.save()
            sekolahasal = sekolahasal_form.save(commit=False)
            sekolahasal.siswa = siswa
            sekolahasal.save()
            jalur = jalur_form.save(commit=False)
            jalur.siswa = siswa
            jalur.save()
            domisili = domisili_form.save(commit=False)
            domisili.siswa = siswa
            domisili.save()
            bantuansosial = bantuansosial_form.save(commit=False)
            bantuansosial.siswa = siswa
            bantuansosial.save()
            dokumen = dokumen_form.save(commit=False)
            dokumen.siswa = siswa
            dokumen.save()
            messages.success(request, 'Data pendaftaran berhasil disimpan.')
            return render(request, 'siswa/formulir.html', {
                'siswa_form': siswa_form,
                'orangtua_form': orangtua_form,
                'wali_form': wali_form,
                'sekolahasal_form': sekolahasal_form,
                'jalur_form': jalur_form,
                'domisili_form': domisili_form,
                'bantuansosial_form': bantuansosial_form,
                'dokumen_form': dokumen_form,
                'success': True
            })
        else:
            messages.error(request, 'Terdapat kesalahan pada form. Silakan periksa kembali.')
    else:
        siswa_form = SiswaForm(instance=siswa_instance)
        orangtua_form = OrangTuaForm(instance=orangtua_instance)
        wali_form = WaliForm(instance=wali_instance)
        sekolahasal_form = SekolahAsalForm(instance=sekolahasal_instance)
        jalur_form = JalurPendaftaranForm(instance=jalur_instance)
        domisili_form = DomisiliForm(instance=domisili_instance)
        bantuansosial_form = BantuanSosialForm(instance=bantuansosial_instance)
        dokumen_form = DokumenForm()
    return render(request, 'siswa/formulir.html', {
        'siswa_form': siswa_form,
        'orangtua_form': orangtua_form,
        'wali_form': wali_form,
        'sekolahasal_form': sekolahasal_form,
        'jalur_form': jalur_form,
        'domisili_form': domisili_form,
        'bantuansosial_form': bantuansosial_form,
        'dokumen_form': dokumen_form
    })

@login_required
def upload(request):
    return render(request, 'siswa/upload.html')

@login_required
def pengumuman(request):
    return render(request, 'siswa/pengumuman.html')
