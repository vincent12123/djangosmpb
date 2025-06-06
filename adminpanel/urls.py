from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # path('siswa/<int:pk>/', views.siswa_detail, name='siswa_detail'),
    # path('verifikasi/<int:pk>/', views.verifikasi_siswa, name='verifikasi_siswa'),
]
