from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime
from app import db

class BaseModel(db.Model):
    """Base model dengan id dan timestamp."""
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

class User(BaseModel):
    __table_args__ = (
        db.UniqueConstraint('email', name='uq_user_email'),
    )
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'siswa' atau 'admin'
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expires = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)  # Status aktif user
    
    def check_password(self, password):
        """Memeriksa apakah password cocok."""
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password, password)
    
    def get_id(self):
        """Diperlukan untuk Flask-Login."""
        return str(self.id)
    
    @property
    def is_authenticated(self):
        """Diperlukan untuk Flask-Login."""
        return True
    
    @property
    def is_anonymous(self):
        """Diperlukan untuk Flask-Login."""
        return False
    
    @property
    def is_admin(self):
        """Cek apakah user adalah admin berdasarkan role."""
        return self.role == 'admin'

# Definisi model siswa jika belum ada
class Siswa(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nama_lengkap = db.Column(db.String(100), nullable=False)
    nisn = db.Column(db.String(20), nullable=False, unique=True)
    nik = db.Column(db.String(20), nullable=False, unique=True)
    tempat_lahir = db.Column(db.String(50), nullable=False)
    tanggal_lahir = db.Column(db.Date, nullable=False)
    jenis_kelamin = db.Column(db.String(10), nullable=False)
    agama = db.Column(db.String(20), nullable=False)
    alamat = db.Column(db.Text, nullable=False)
    telepon = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    status_pendaftaran = db.Column(db.String(20), default='draft', nullable=False)  # Tambahkan baris ini
    orang_tua = db.relationship('OrangTua', backref='siswa', uselist=False)
    sekolah_asal = db.relationship('SekolahAsal', backref='siswa', uselist=False)
    dokumen = db.relationship('Dokumen', backref='siswa')
    verifikasi = db.relationship('Verifikasi', backref='siswa', uselist=False)

class OrangTua(BaseModel):
    siswa_id = db.Column(db.Integer, db.ForeignKey('siswa.id'), nullable=False)
    nama_ayah = db.Column(db.String(100), nullable=False)
    nama_ibu = db.Column(db.String(100), nullable=False)
    pekerjaan_ayah = db.Column(db.String(50), nullable=False)
    pekerjaan_ibu = db.Column(db.String(50), nullable=False)
    telepon_ayah = db.Column(db.String(15), nullable=False)
    telepon_ibu = db.Column(db.String(15), nullable=False)

class SekolahAsal(BaseModel):
    siswa_id = db.Column(db.Integer, db.ForeignKey('siswa.id'), nullable=False)
    nama_sekolah = db.Column(db.String(100), nullable=False)
    alamat_sekolah = db.Column(db.Text, nullable=False)
    tahun_lulus = db.Column(db.Integer, nullable=False)

class Dokumen(BaseModel):
    siswa_id = db.Column(db.Integer, db.ForeignKey('siswa.id'), nullable=False)
    jenis_dokumen = db.Column(db.String(50), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='Diupload')  # 'Diupload', 'Diverifikasi', 'Ditolak'

class Verifikasi(BaseModel):
    siswa_id = db.Column(db.Integer, db.ForeignKey('siswa.id'), nullable=False)
    status = db.Column(db.String(20), default='Menunggu')  # 'Menunggu', 'Disetujui', 'Ditolak'
    catatan = db.Column(db.Text)
    tanggal_verifikasi = db.Column(db.DateTime, default=datetime.utcnow)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Tambahkan baris ini

class Soal(BaseModel):
    """Model untuk soal tes masuk SPMB."""
    pertanyaan = db.Column(db.Text, nullable=False)
    tipe = db.Column(db.String(20), nullable=False, default='pilihan_ganda')  # 'pilihan_ganda' atau 'isian'
    pilihan_a = db.Column(db.String(255), nullable=True)
    pilihan_b = db.Column(db.String(255), nullable=True)
    pilihan_c = db.Column(db.String(255), nullable=True)
    pilihan_d = db.Column(db.String(255), nullable=True)
    pilihan_e = db.Column(db.String(255), nullable=True)  # untuk soal pilihan ganda dengan 5 opsi
    jawaban_benar = db.Column(db.String(10), nullable=False)  # contoh: 'A', 'B', 'C', 'D' atau jawaban isian
    aktif = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Soal {self.id}: {self.pertanyaan[:30]}...>"

# Contoh model untuk menyimpan jawaban siswa (opsional, jika ingin tracking hasil tes)
class JawabanSiswa(BaseModel):
    siswa_id = db.Column(db.Integer, db.ForeignKey('siswa.id'), nullable=False)
    soal_id = db.Column(db.Integer, db.ForeignKey('soal.id'), nullable=False)
    jawaban = db.Column(db.String(255), nullable=False)
    benar = db.Column(db.Boolean, nullable=True)  # True jika jawaban benar

    soal = db.relationship('Soal', backref='jawaban_siswa')
    siswa = db.relationship('Siswa', backref='jawaban_soal')
