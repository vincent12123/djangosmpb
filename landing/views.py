from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render
import time
import uuid
from django.views.decorators.http import require_POST
import os
from google import genai

from django.conf import settings

def get_gemini_model():
    api_key = getattr(settings, 'GEMINI_API_KEY', None) or os.environ.get('GEMINI_API_KEY')
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.8,
        "top_k": 40,
        "max_output_tokens": 1024,
        "response_mime_type": "text/plain",
    }
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]
    model_name = getattr(settings, 'GEMINI_MODEL', 'gemini-2.0-flash-exp')
    system_prompt = """
Anda adalah asisten virtual untuk Sistem Penerimaan Murid Baru (SPMB) SMP Negeri 2 Sintang.

INFORMASI SEKOLAH:
- Nama: SMP Negeri 2 Sintang
- Alamat: Jl. Letjend MT Haryono, RT 14/RW 4
- Desa/Kelurahan: Kapuas Kanan Hulu, Kec. Sintang
- Kab. Sintang, Kalimantan Barat 78614
- Telepon: +62 561 1234567
- Email: spmb@smpn2sintang.sch.id

JADWAL PPDB 2025:
- Pendaftaran: SEDANG BUKA! (Bisa mendaftar sekarang)
- Jadwal lengkap akan diumumkan di dashboard siswa setelah registrasi

PERSYARATAN PENDAFTARAN:
- Ijazah/SKHUN SD atau yang setara
- Akta kelahiran
- Kartu Keluarga (KK)
- Pas foto 3x4 (2 lembar)
- Rapor kelas 4, 5, dan 6 SD
- Surat keterangan sehat & berkelakuan baik

JALUR PENERIMAAN:
1. Jalur Zonasi (50% kuota)
2. Jalur Afirmasi (15% kuota) - untuk siswa dari keluarga ekonomi tidak mampu
3. Jalur Mutasi (5% kuota) - untuk anak guru/tenaga kependidikan
4. Jalur Prestasi (30% kuota) - berdasarkan nilai rapor dan prestasi

BIAYA:
- Pendaftaran: GRATIS
- SPP: GRATIS (sekolah negeri)
- Seragam dan buku: ditanggung komite sekolah

CARA PENDAFTARAN ONLINE:
1. Buka website sekolah
2. Klik "Daftar Sekarang"
3. Buat akun siswa dengan email aktif
4. Login dan isi formulir pendaftaran
5. Upload dokumen persyaratan
6. Submit dan tunggu verifikasi admin
7. Pantau status di dashboard siswa

ATURAN RESPONS:
- Jawab dalam bahasa Indonesia yang sopan dan ramah
- Gunakan format Markdown untuk formatting yang lebih baik
- Gunakan bold untuk penekanan penting
- Gunakan bullet points (-) untuk daftar
- Gunakan numbered lists (1.) untuk langkah-langkah
- Maksimal 3 paragraf per respons
- Gunakan emoji yang sesuai 🎓📚✅
- Selalu tawarkan bantuan lebih lanjut
"""
    return genai.GenerativeModel(
        model_name=model_name,
        generation_config=generation_config,
        safety_settings=safety_settings,
        system_instruction=system_prompt
    )

@csrf_exempt
@require_POST
def api_chat(request):
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id')
        if not user_message:
            return JsonResponse({
                'success': False,
                'error': 'Pesan tidak boleh kosong'
            }, status=400)
        if len(user_message) > 500:
            return JsonResponse({
                'success': False,
                'error': 'Pesan terlalu panjang (maksimal 500 karakter)'
            }, status=400)
        if not session_id:
            session_id = str(uuid.uuid4())
        start_time = time.time()
        # --- INTEGRASI GEMINI ASLI ---
        model = get_gemini_model()
        if not model:
            return JsonResponse({
                'success': False,
                'error': 'Gemini API key tidak ditemukan atau model gagal diinisialisasi',
                'fallback_response': 'Maaf, layanan AI tidak tersedia. Hubungi admin sekolah.'
            }, status=503)
        try:
            response = model.generate_content(user_message)
            if hasattr(response, 'text'):
                gemini_response = response.text.strip()
            else:
                gemini_response = str(response)
        except Exception as e:
            gemini_response = 'Maaf, terjadi kesalahan saat menghubungi AI. Silakan coba lagi.'
        # --- END INTEGRASI ---
        response_time = time.time() - start_time
        return JsonResponse({
            'success': True,
            'response': gemini_response,
            'source': 'gemini',
            'session_id': session_id,
            'response_time': round(response_time, 2),
            'format': 'markdown'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'Internal server error',
            'fallback_response': 'Maaf, terjadi kesalahan sistem. Silakan coba lagi atau hubungi admin sekolah di +62 561 1234567.'
        }, status=500)

# Create your views here.
def landing(request):
    return render(request, 'landing/index.html')
