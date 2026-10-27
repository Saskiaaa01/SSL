# SSLGuard 🛡️
### SSL/TLS Certificate Monitoring & WhatsApp Alert System

> Sistem Pemantauan Masa Berlaku Sertifikat SSL/TLS & Notifikasi Peringatan Dini WhatsApp  
> **Program Praktik Kerja Lapangan (PKL) 2026 — Dinas Komunikasi dan Informatika (KOMINFO)**

---

## 📌 Ringkasan Proyek

**SSLGuard** adalah sistem pemantauan proaktif terhadap masa berlaku dan validitas sertifikat SSL/TLS untuk seluruh portal website dan subdomain instansi pemerintah binaan KOMINFO. Sistem ini secara otomatis menginspeksi sertifikat publik via TLS Handshake nyata, memvalidasi Common Name (CN) & Subject Alternative Names (SANs), mendeteksi proteksi SSRF, serta mengirimkan peringatan berjenjang via **WhatsApp Cloud API** pada ambang batas **H-30, H-14, dan H-7** kepada Administrator dan Pemilik Domain (*Owner*).

---

## 🏗️ Struktur Arsitektur & Direktori Proyek

Proyek ini dibangun menggunakan arsitektur modular berlapis (*Clean Layered Architecture*):

```text
SSLGuard/
├── backend/                             # REST API & Inspection Engine (Python FastAPI)
│   ├── app/
│   │   ├── api/                         # Routing & Dependencies
│   │   │   ├── deps.py                  # JWT Auth & RBAC Dependency Injection
│   │   │   └── v1/
│   │   │       ├── api.py               # Router Agregator v1
│   │   │       └── endpoints/
│   │   │           ├── auth.py          # /api/v1/auth (Login & Sesi JWT)
│   │   │           ├── websites.py      # /api/v1/websites (CRUD Domain & On-Demand Scan)
│   │   │           ├── dashboard.py     # /api/v1/dashboard (Statistik & Mass Scan)
│   │   │           ├── notifications.py # /api/v1/notifications (Log Audit & Uji WA)
│   │   │           ├── users.py         # /api/v1/users (Manajemen Pengguna)
│   │   │           └── reports.py       # /api/v1/reports (Ekspor CSV dengan UTF-8 BOM)
│   │   ├── core/                        # Konfigurasi Inti
│   │   │   ├── config.py                # Pydantic Settings (.env loader)
│   │   │   ├── database.py              # Engine SQLAlchemy & Session Factory
│   │   │   └── security.py              # Enkripsi bcrypt & JWT HS256
│   │   ├── models/                      # SQLAlchemy ORM Models
│   │   │   ├── user.py                  # Model Pengguna & Role
│   │   │   ├── website.py               # Model Domain Terdaftar
│   │   │   ├── ssl_check.py             # Model Riwayat Inspeksi Sertifikat x509
│   │   │   └── notification.py          # Model Log Audit WhatsApp
│   │   ├── schemas/                     # Pydantic v2 Request/Response Validation
│   │   │   ├── user.py
│   │   │   ├── website.py
│   │   │   ├── ssl_check.py
│   │   │   ├── notification.py
│   │   │   └── dashboard.py
│   │   ├── services/                    # Business Logic Engines
│   │   │   ├── ssl_checker.py           # Real TLS Handshake, x509 Parser & SSRF Guard
│   │   │   ├── whatsapp.py              # WhatsApp Cloud API & Anti-Spam Idempotency
│   │   │   └── scheduler.py             # APScheduler Rutin Harian (07:00 WIB)
│   │   └── main.py                      # FastAPI App, CORS, Lifespan & SPA Static Mount
│   ├── requirements.txt                 # Dependensi Python Terkunci
│   ├── .env.example                     # Templat Variabel Lingkungan
│   ├── seed_data.py                     # Seeder Basis Data (Akun Demo & Domain Awal)
│   └── run.py                           # Runner Mandiri Backend
├── frontend/                            # Modern Glassmorphism Single Page Application
│   ├── index.html                       # Antarmuka Dashboard Interaktif
│   ├── style.css                        # Design System Cyber-Security (Neon Blue / Dark)
│   └── app.js                           # Controller Hybrid (Live REST API + Fallback Demo)
├── Dokumen/                             # Dokumen Rekayasa Perangkat Lunak Resmi
│   ├── md/
│   │   ├── BRD_SSLGuard_SSL_Checker.md  # Business Requirements Document
│   │   ├── SRS_SSLGuard_SSL_Checker.md  # Software Requirements Specification
│   │   └── FSD_SSLGuard_SSL_Checker.md  # Functional Specification Document
│   └── *.docx                           # Berkas Dokumen Word Asli
├── PSD_SSLGuard_SSL_Checker.md          # Product Specification Document Terpadu
├── run.py                               # Runner Utama (All-in-One Launcher)
├── start.bat                            # Shortcut Eksekusi Windows (Double Click)
└── .gitignore                           # Filter Berkas Repository
```

---

## ⚡ Cara Menjalankan Proyek (Quick Start)

### 1. Prasyarat Sistem
- **Python 3.11+** (Disarankan Python 3.11)
- Akses internet (untuk inspeksi SSL langsung ke domain publik)

### 2. Instalasi & Menjalankan (Pilihan A: Otomatis 1-Klik)

Cukup jalankan berkas runner utama:
```bash
python run.py
```
*Atau klik dua kali berkas `start.bat` pada Windows Explorer.*

Runner akan otomatis:
1. Memeriksa virtual environment (`venv`).
2. Menginisialisasi basis data `sslguard.db` dan menjalankan seeder jika belum ada.
3. Menjalankan server backend FastAPI sekaligus menyajikan frontend SPA di alamat:
   - **Dashboard Aplikasi:** [http://localhost:8000/](http://localhost:8000/)
   - **Dokumentasi Interaktif Swagger:** [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Alternatif ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

### 3. Pilihan B: Instalasi Manual (Langkah demi Langkah)

1. Buat dan aktifkan virtual environment:
   ```bash
   python -m venv venv
   # Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   # Linux / macOS:
   source venv/bin/activate
   ```

2. Instal dependensi:
   ```bash
   pip install -r backend/requirements.txt
   ```

3. Jalankan inisialisasi basis data:
   ```bash
   python backend/seed_data.py
   ```

4. Jalankan backend:
   ```bash
   python backend/run.py
   ```

---

## 🔐 Akun Uji Coba & Kredensial Demo

| Akun / Role | Username / Email | Password | Hak Akses |
| :--- | :--- | :--- | :--- |
| **Super Admin** | `admin@kominfo.go.id` *(atau ketik `admin`)* | `Admin@2026` | Akses penuh seluruh domain, manajemen user, ekspor laporan, dan trigger inspeksi. |
| **Owner (Diskominfo)** | `budi@dinas.go.id` *(atau ketik `budi`)* | `Budi@2026` | Akses monitoring khusus domain unit kerja Diskominfo. |
| **Owner (Bag. Hukum)** | `siti@hukum.kota.go.id` *(atau ketik `siti`)* | `Siti@2026` | Akses monitoring khusus domain JDIH / Bagian Hukum. |
| **Owner (BKPSDM)** | `agus@bkpsdm.kab.go.id` *(atau ketik `agus`)* | `Agus@2026` | Akses monitoring domain BKPSDM. |

---

## 🚀 Fitur Unggulan

1. **SSL/TLS Live Inspection Engine:** Mengambil sertifikat publik x509 langsung melalui TLS Handshake socket riil, mengekstrak penerbit (CA), tanggal berlaku, sisa hari, SANs, serial, dan sidik jari SHA-256.
2. **SSRF Protection:** Validasi nama host ketat yang memblokir alamat IP privat, loopback (127.0.0.1), dan link-local cloud metadata.
3. **Multi-Threshold WhatsApp Alert:** Sistem peringatan proaktif berjenjang pada H-30, H-14, H-7, dan EXPIRED dengan dukungan Meta Cloud API dan mode simulasi realistis.
4. **Anti-Spam Idempotency:** Mencegah pengiriman pesan ganda dalam siklus 24 jam untuk ambang batas yang sama.
5. **Scheduled Task:** Penjadwalan harian otomatis berbasis APScheduler pada pukul **07:00 WIB**.
6. **Ekspor Audit CSV:** Ekspor data seluruh domain lengkap dengan BOM UTF-8 yang langsung rapi terbaca di Microsoft Excel.
7. **Hybrid Client Engine:** Frontend otomatis terhubung ke REST API FastAPI saat server aktif, dengan fallback ke mode simulasi lokal jika offline.

---

## 📚 Dokumen Spesifikasi Rekayasa Perangkat Lunak

| Dokumen | Berkas | Deskripsi |
| :--- | :--- | :--- |
| **PSD** | [PSD_SSLGuard_SSL_Checker.md](PSD_SSLGuard_SSL_Checker.md) | **Product Specification Document:** Spesifikasi terpadu teknis dan bisnis. |
| **BRD** | [Dokumen/md/BRD_SSLGuard_SSL_Checker.md](Dokumen/md/BRD_SSLGuard_SSL_Checker.md) | **Business Requirements Document:** Latar belakang, KPI, dan BPMN. |
| **SRS** | [Dokumen/md/SRS_SSLGuard_SSL_Checker.md](Dokumen/md/SRS_SSLGuard_SSL_Checker.md) | **Software Requirements Specification:** Kebutuhan fungsional FR-01 s.d FR-07 dan ERD. |
| **FSD** | [Dokumen/md/FSD_SSLGuard_SSL_Checker.md](Dokumen/md/FSD_SSLGuard_SSL_Checker.md) | **Functional Specification Document:** Wireframe UI, payload API, dan use case. |

---

## 📄 Lisensi
Hak Cipta © 2026 Tim PKL Dinas Komunikasi dan Informatika (KOMINFO). Seluruh hak cipta dilindungi undang-undang.
