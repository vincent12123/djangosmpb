import os
import json
import time
import uuid

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.conf import settings

from google import genai  # Correct import for new SDK

# --- Gemini Config ---
GEMINI_MODEL = getattr(settings, 'GEMINI_MODEL', 'gemini-2.0-flash-exp')
GEMINI_API_KEY = getattr(settings, 'GEMINI_API_KEY', None) or os.environ.get('GEMINI_API_KEY')

SYSTEM_PROMPT = """
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

def get_gemini_client():
    if not GEMINI_API_KEY:
        return None
    return genai.Client(api_key=GEMINI_API_KEY)

@csrf_exempt
@require_POST
def api_chat(request):
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id')
        
        if not user_message:
            return JsonResponse({'success': False, 'error': 'Pesan tidak boleh kosong'}, status=400)
        if len(user_message) > 500:
            return JsonResponse({'success': False, 'error': 'Pesan terlalu panjang (maksimal 500 karakter)'}, status=400)
        if not session_id:
            session_id = str(uuid.uuid4())
        
        start_time = time.time()
        client = get_gemini_client()
        if not client:
            return JsonResponse({
                'success': False,
                'error': 'Gemini API key tidak ditemukan atau client gagal diinisialisasi',
                'fallback_response': 'Maaf, layanan AI tidak tersedia. Hubungi admin sekolah.'
            }, status=503)
        
        # Compose the full prompt (system + user message)
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_message}\nAssistant:"
        
        gemini_response = 'Maaf, terjadi kesalahan saat menghubungi AI. Silakan coba lagi.'
        try:
            # Use the simplified API call
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=full_prompt
            )
            
            # Extract the text content from the response
            if hasattr(response, 'text'):
                gemini_response = response.text.strip()
            elif hasattr(response, 'candidates') and response.candidates:
                # Try to extract from candidates
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                    gemini_response = candidate.content.parts[0].text.strip()
                else:
                    gemini_response = str(candidate)
            else:
                gemini_response = str(response)
                
        except Exception as e:
            print(f"Gemini API error: {str(e)}")
            gemini_response = f'Maaf, terjadi kesalahan saat menghubungi AI: {str(e)}'
        
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
        print(f"Chat API error: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': f'Internal server error: {str(e)}',
            'fallback_response': 'Maaf, terjadi kesalahan sistem. Silakan coba lagi atau hubungi admin sekolah di +62 561 1234567.'
        }, status=500)

# Optional: Health check endpoint
@csrf_exempt
def api_chat_health(request):
    try:
        client = get_gemini_client()
        if client:
            # Test with a simple prompt
            test_response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents="Hello"
            )
            return JsonResponse({
                'status': 'healthy', 
                'message': 'Gemini AI service is available', 
                'timestamp': time.time()
            })
        else:
            return JsonResponse({
                'status': 'degraded', 
                'message': 'Gemini AI service is not available', 
                'timestamp': time.time()
            })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy', 
            'message': f'Error: {str(e)}', 
            'timestamp': time.time()
        })

def landing(request):
    return render(request, 'landing/index.html')
