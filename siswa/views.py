from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'siswa/dashboard.html')

@login_required
def status(request):
    return render(request, 'siswa/status.html')

@login_required
def formulir(request):
    return render(request, 'siswa/formulir.html')

@login_required
def upload(request):
    return render(request, 'siswa/upload.html')

@login_required
def pengumuman(request):
    return render(request, 'siswa/pengumuman.html')
