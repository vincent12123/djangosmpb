# SMP Negeri 2 PPDB (Penerimaan Peserta Didik Baru)

A Django web app for student admission with:
- SEO landing page
- Registration & login
- Student dashboard (status, registration form, document upload, announcements)
- Registration form fields follow Dapodik SMP Indonesia

## Progress & Status
### ✅ Sudah dilakukan
- Migrasi model dari Flask/SQLAlchemy ke Django ORM (User, Siswa, OrangTua, SekolahAsal, Dokumen, Verifikasi, Soal, JawabanSiswa)
- Implementasi custom User model (AUTH_USER_MODEL) untuk autentikasi Django
- Semua model sudah didaftarkan ke admin Django (bisa dikelola via /admin)
- Halaman login, register, dashboard siswa, dan landing page sudah tersedia
- Struktur app modular: landing, accounts, siswa

### ❌ Belum/tahap berikutnya
- Formulir pendaftaran siswa sesuai Dapodik SMP Indonesia (field lengkap, validasi, dsb)
- Fitur upload dokumen siswa (form & proses upload)
- Fitur pengumuman hasil seleksi (otomatisasi, notifikasi)
- Integrasi email (aktivasi, reset password, dsb)
- Penambahan SEO meta tags lanjutan
- Uji coba dan deployment ke server produksi

## Setup
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Jalankan migrasi database:
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Buat superuser (admin):
   ```sh
   python manage.py createsuperuser
   ```
4. Start the server:
   ```sh
   python manage.py runserver
   ```

## Apps
- `landing`: Landing page & SEO
- `accounts`: Registration, login, authentication, custom user
- `siswa`: Student dashboard, registration form, document upload, announcements

## Next Steps
- Implement registration form fields as per Dapodik SMP
- Build dashboard sidebar & features
- Add Google SEO meta tags to landing page
