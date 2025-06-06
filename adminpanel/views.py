from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from siswa.models import Siswa

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or getattr(request.user, 'role', None) != 'admin':
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden('Hanya admin/operator yang boleh mengakses halaman ini.')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@login_required
@admin_required
def dashboard(request):
    siswa_list = Siswa.objects.all()
    return render(request, 'adminpanel/dashboard.html', {'siswa_list': siswa_list})
