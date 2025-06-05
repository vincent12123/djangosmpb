from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('status/', views.status, name='status'),
    path('formulir/', views.formulir, name='formulir'),
    path('upload/', views.upload, name='upload'),
    path('pengumuman/', views.pengumuman, name='pengumuman'),
]
