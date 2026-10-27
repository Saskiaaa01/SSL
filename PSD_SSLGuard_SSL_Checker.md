# DOKUMEN SPESIFIKASI BISNIS DAN TEKNIS REKAYASA SISTEM TERPADU
## **PRODUCT SPECIFICATION DOCUMENT (PSD)**
# **SSLGUARD: SSL Certificate Monitoring & WhatsApp Alert System**

**Nomor Dokumen:** PSD-SSLGUARD-2026-001  
**Versi:** 1.0  
**Tanggal Terbit:** Oktober 2026  
**Status:** Disetujui (Approved)  
**Klasifikasi:** Internal — Program PKL 2026  
**Pemilik Produk (Product Owner):** Dinas Komunikasi dan Informatika (KOMINFO)  
**Penyusun:** Tim Pengembang PKL 2026 - KOMINFO  
**Disetujui Oleh:** Pembimbing Lapangan KOMINFO  

---

## DAFTAR ISI

1. [RINGKASAN EKSEKUTIF PRODUK](#1-ringkasan-eksekutif-produk)
2. [KONTEKS BISNIS DAN NILAI STRATEGIS](#2-konteks-bisnis-dan-nilai-strategis)
3. [DESKRIPSI PRODUK DAN ARSITEKTUR SISTEM](#3-deskripsi-produk-dan-arsitektur-sistem)
4. [SPESIFIKASI FUNGSIONAL TEKNIS](#4-spesifikasi-fungsional-teknis)
5. [SPESIFIKASI BASIS DATA (DATABASE DESIGN)](#5-spesifikasi-basis-data)
6. [KONTRAK ANTARMUKA API (API CONTRACT)](#6-kontrak-antarmuka-api)
7. [SPESIFIKASI ANTARMUKA PENGGUNA (UI/UX SPECIFICATION)](#7-spesifikasi-antarmuka-pengguna)
8. [SPESIFIKASI NON-FUNGSIONAL](#8-spesifikasi-non-fungsional)
9. [ALUR LOGIKA & STATE MACHINE SISTEM](#9-alur-logika--state-machine-sistem)
10. [RENCANA IMPLEMENTASI & MILESTONE](#10-rencana-implementasi--milestone)
11. [MATRIKS KETERTELUSURAN TERPADU](#11-matriks-ketertelusuran-terpadu)
12. [GLOSARIUM DAN REFERENSI](#12-glosarium-dan-referensi)

---

## 1. RINGKASAN EKSEKUTIF PRODUK

**SSLGuard** adalah platform perangkat lunak berbasis web (*web-based software*) yang dirancang khusus untuk memecahkan permasalahan kritis pengelolaan infrastruktur keamanan digital di lingkungan Dinas Komunikasi dan Informatika (KOMINFO). Produk ini berfungsi sebagai **Centralized SSL/TLS Certificate Monitoring & Early Warning System** yang mengintegrasikan kemampuan pemindaian sertifikat otomatis dengan saluran notifikasi WhatsApp.

### Ringkasan Masalah yang Dipecahkan:
Puluhan domain website layanan publik pemerintah memiliki sertifikat SSL/TLS dengan masa berlaku terbatas. Keterlambatan pembaruan mengakibatkan peramban memunculkan peringatan keras (*"Your connection is not private"*) yang memblokir akses masyarakat dan merusak kredibilitas instansi.

### Solusi yang Ditawarkan SSLGuard:

| Dimensi | Kondisi Sebelum | Kondisi Sesudah SSLGuard |
|---|---|---|
| **Pemantauan** | Manual, per-domain, tidak terpusat | Otomatis, terpusat, semua domain sekaligus |
| **Notifikasi** | Email (sering terlewat) | WhatsApp langsung ke HP pengelola |
| **Waktu Peringatan** | Reaktif (setelah expired) | Proaktif H-30, H-14, H-7 |
| **Duplikasi Pesan** | Tidak terkontrol | Anti-spam idempotency per siklus |
| **Visibilitas** | Tidak ada dashboard | Dashboard real-time lengkap |

### Dokumen Terkait:

| Dokumen | Nomor | Fokus |
|---|---|---|
| BRD | BRD-SSLGUARD-2026-001 | Kebutuhan & nilai bisnis |
| SRS | SRS-SSLGUARD-2026-001 | Spesifikasi kebutuhan perangkat lunak |
| FSD | FSD-SSLGUARD-2026-001 | Desain fungsional & UI wireframe |
| **PSD (dokumen ini)** | **PSD-SSLGUARD-2026-001** | **Spesifikasi bisnis & teknis terpadu** |

---

## 2. KONTEKS BISNIS DAN NILAI STRATEGIS

### 2.1 Pernyataan Masalah (Problem Statement)

#### Akar Masalah (Root Cause Analysis — 5 Whys):

```
Masalah: Website pemerintah expired SSL → akses publik terblokir
  ↳ Mengapa? → Admin tidak mengetahui sertifikat hampir expired
    ↳ Mengapa? → Tidak ada sistem monitoring terpusat
      ↳ Mengapa? → Pengelolaan dilakukan manual per-unit kerja
        ↳ Mengapa? → Tidak ada standar prosedur monitoring SSL
          ↳ Mengapa? → Kebutuhan belum pernah diformulasikan sebagai proyek TI
```

#### Evidensi Masalah:
- **Waktu Deteksi Rata-rata:** 6–24 jam setelah sertifikat expired
- **Sumber Notifikasi Saat Ini:** Email dari penyedia hosting yang sering masuk spam
- **Jumlah Domain Terdampak Potensi:** 50+ domain aktif unit kerja KOMINFO
- **Kerugian per Insiden:** Penurunan kepercayaan publik + beban kerja reaktif tim IT

### 2.2 Visi dan Misi Produk

> **Visi:** Menjadi sistem sentinel digital terdepan yang menjamin ketersediaan dan kepercayaan seluruh layanan online KOMINFO melalui pemantauan SSL/TLS yang proaktif, otomatis, dan cerdas.

> **Misi:** Mengembangkan platform monitoring SSL berbasis web yang ringan, handal, dan terintegrasi dengan WhatsApp untuk memastikan tidak ada satu pun domain instansi yang mengalami insiden expired certificate akibat kelalaian manusia.

### 2.3 Nilai Bisnis (Business Value Proposition)

#### Nilai Terukur (Quantifiable Value):

| Metrik | Estimasi Nilai |
|---|---|
| **Pengurangan insiden SSL expired** | 95–100% (target 0 insiden/tahun) |
| **Penghematan waktu monitoring manual** | ~8 jam/minggu/admin |
| **Waktu respons insiden** | Dari 6–24 jam → < 5 menit (notifikasi proaktif) |
| **Cakupan domain terpantau** | 100% domain terdaftar, 24/7/365 |
| **ROI Operasional** | Tidak ada biaya lisensi (open-source stack) |

### 2.4 Indikator Keberhasilan Produk (KPI & OKR)

#### Key Performance Indicators (KPI):

| KPI | Definisi | Target | Cara Ukur |
|---|---|---|---|
| **KPI-01** | Tingkat deteksi tepat waktu | 100% domain terdeteksi sebelum H-7 | Log monitoring scheduler |
| **KPI-02** | Uptime scheduler | >= 99.5% scheduler berhasil berjalan | Log APScheduler |
| **KPI-03** | Akurasi sisa hari | Error <= 1 hari dari kondisi aktual | Verifikasi manual vs sistem |
| **KPI-04** | Tingkat pengiriman WA | >= 98% pesan terkirim ke penerima | Log WhatsApp API response |
| **KPI-05** | Waktu pemindaian per domain | <= 5 detik/domain | Profiling SSL handshake |
| **KPI-06** | Zero false positive expired | 0 notifikasi salah kirim | Audit log notifikasi |

---

## 3. DESKRIPSI PRODUK DAN ARSITEKTUR SISTEM

### 3.1 Gambaran Umum Produk

SSLGuard adalah aplikasi web tiga-lapisan (*three-tier web application*) dengan komponen:
1. **Frontend** — Dashboard SPA (Single Page Application) berbasis HTML/CSS/JavaScript murni
2. **Backend** — REST API server berbasis Python FastAPI
3. **Database** — PostgreSQL sebagai basis data relasional utama

### 3.2 Arsitektur Sistem (System Architecture)

```
+-------------------------------------------------------------------------+
|                          INTERNET / INTRANET                            |
+----------------------------------+--------------------------------------+
                                   |
              +--------------------v-----------------------+
              |          NGINX Reverse Proxy               |
              |     (HTTPS termination, static files)      |
              +--------+-----------------------------------+
                       |
       +---------------v------------------+
       |         FRONTEND LAYER           |
       |   HTML + CSS + Vanilla JS SPA    |
       |   - Login Page                   |
       |   - Dashboard View               |
       |   - Website Management View      |
       |   - WhatsApp Log View            |
       |   - User Management View         |
       +----------------+-----------------+
                        |  REST API (JSON/HTTPS)
       +----------------v-----------------+
       |         BACKEND LAYER            |
       |       FastAPI (Python 3.11)      |
       |   +-------------------------+    |
       |   |  Router: /api/auth      |    |
       |   |  Router: /api/websites  |    |
       |   |  Router: /api/notify    |    |
       |   |  Router: /api/logs      |    |
       |   |  Router: /api/users     |    |
       |   +------------+------------+    |
       |                |                 |
       |   +------------v------------+    |
       |   |   SSL INSPECTION ENGINE |    |
       |   |  (ssl.SSLContext + x509)|    |
       |   +------------+------------+    |
       |                |                 |
       |   +------------v------------+    |
       |   |   APScheduler (CRON)    |    |
       |   |   Trigger: 07:00 WIB   |    |
       |   +------------+------------+    |
       +----------------+-----------------+
                        |
       +----------------v-----------------+
       |         DATA LAYER               |
       |      PostgreSQL 15+              |
       |   +-------------------------+    |
       |   | Tables:                 |    |
       |   | - users                 |    |
       |   | - websites              |    |
       |   | - ssl_check_results     |    |
       |   | - notification_logs     |    |
       |   | - notification_rules    |    |
       |   +-------------------------+    |
       +----------------------------------+
                        |
       +----------------v-----------------+
       |     EXTERNAL SERVICES            |
       |  WhatsApp Cloud API (Meta)       |
       |  (HTTPS POST ke graph.facebook)  |
       +----------------------------------+
```

### 3.3 Tumpukan Teknologi (Technology Stack)

#### Backend:
```
Python              3.11+
FastAPI             0.111+
Uvicorn             0.29+ (ASGI server)
SQLAlchemy          2.0+ (ORM)
Alembic             1.13+ (Database migration)
python-jose         3.3+ (JWT token)
passlib[bcrypt]     1.7.4+
APScheduler         3.10+
cryptography        42.0+ (x509 parsing)
httpx               0.27+ (async HTTP client)
pydantic            2.x
psycopg2-binary     2.9+
python-dotenv       1.0+
```

#### Frontend:
```
HTML5               Semantic markup
CSS3                Custom design system (glassmorphism + neon blue)
JavaScript          ES2022+ (Vanilla, no framework)
Google Fonts        Inter, Outfit, JetBrains Mono
```

#### Infrastructure:
```
PostgreSQL          15+
Nginx               1.25+
Docker              24+ (opsional)
Git / GitHub        Version control
```

---

## 4. SPESIFIKASI FUNGSIONAL TEKNIS

### 4.1 Modul Autentikasi & RBAC

#### Role-Based Access Control (RBAC):

| Role | Hak Akses |
|---|---|
| **SUPER_ADMIN** | Full CRUD semua entitas + manajemen user + konfigurasi sistem |
| **ADMIN** | CRUD website, trigger pemindaian manual, lihat semua log |
| **VIEWER** | Read-only: lihat dashboard, website list, log notifikasi |

#### Spesifikasi Keamanan:
- JWT HS256, Access Token expire 60 menit, Refresh Token 7 hari
- bcrypt hashing dengan salt factor 12
- Rate limiting login: maks 5 kali gagal dalam 10 menit → lock 15 menit
- CORS policy: hanya origin terdaftar

### 4.2 Modul SSL/TLS Inspection Engine

#### Kategori Status Sertifikat:

| Status Kode | Kondisi | Warna UI | Aksi Triggered |
|---|---|---|---|
| `VALID` | days_remaining > 30 | Hijau | Tidak ada notifikasi |
| `WARNING_30` | 15 < days_remaining <= 30 | Kuning | Notifikasi H-30 |
| `WARNING_14` | 7 < days_remaining <= 14 | Oranye | Notifikasi H-14 |
| `CRITICAL_7` | 0 < days_remaining <= 7 | Merah | Notifikasi H-7 (setiap hari) |
| `EXPIRED` | days_remaining <= 0 | Hitam-Merah | Notifikasi darurat |
| `FAILED` | Koneksi gagal/timeout | Abu-abu | Log error, tidak kirim WA |

#### Data Sertifikat yang Diekstrak:
```python
SSLCheckResult:
    domain, issuer, subject_cn,
    valid_from, expires_at, days_remaining,
    fingerprint (SHA-256), serial_number,
    sans (Subject Alt Names), chain_valid,
    hostname_match, status, checked_at
```

### 4.3 Modul Scheduler & Task Engine

#### Konfigurasi:
```python
scheduler = BackgroundScheduler(timezone="Asia/Jakarta")
scheduler.add_job(
    func      = run_daily_monitoring_job,
    trigger   = CronTrigger(hour=7, minute=0),  # 07:00 WIB
    id        = "ssl_daily_monitor",
    misfire_grace_time = 3600  # toleransi 1 jam jika server sempat mati
)
```

### 4.4 Modul Alert Evaluation & Anti-Spam (Idempotency)

#### Aturan Threshold Notifikasi:

| Threshold | Zona Hari | Frekuensi Notifikasi |
|---|---|---|
| WARNING_30 | 15–30 hari | Sekali per siklus |
| WARNING_14 | 7–14 hari | Sekali per siklus |
| CRITICAL_7 | 0–7 hari | Setiap hari (harian) |
| EXPIRED | <= 0 hari | Setiap hari (darurat) |

### 4.5 Modul Notifikasi WhatsApp

#### Template Pesan Kritis (H-7):
```
[SSLGuard] PERINGATAN KRITIS — 5 HARI LAGI!

Domain: portal.dinas.go.id
Sisa Waktu: 5 hari
Kedaluwarsa: 23 November 2026
Unit Kerja: Diskominfo

TINDAKAN SEGERA DIPERLUKAN! Sertifikat SSL akan kedaluwarsa
dalam waktu sangat singkat.

Dikirim otomatis oleh SSLGuard KOMINFO
```

---

## 5. SPESIFIKASI BASIS DATA

### 5.1 Entity-Relationship Diagram (ERD)

```
+-------------+       +------------------+       +------------------+
|    users    |       |     websites     |       | ssl_check_results|
|-------------|       |------------------|       |------------------|
| id (PK)     +------<+ created_by (FK)  |       | id (PK)          |
| username    |       | id (PK)          +>------+ website_id (FK)  |
| email       |       | domain           |       | checked_at       |
| password_hash       | port             |       | status           |
| full_name   |       | owner_name       |       | days_remaining   |
| role        |       | owner_wa         |       | expires_at       |
| is_active   |       | is_active        |       | valid_from       |
| created_at  |       | created_at       |       | issuer           |
| last_login  |       | updated_at       |       | fingerprint      |
+-------------+       +--------+---------+       | hostname_match   |
                               |                 | error_message    |
                       +-------v----------+       +------------------+
                       |notification_logs |
                       |------------------|
                       | id (PK)          |
                       | website_id (FK)  |
                       | threshold_label  |
                       | recipient_wa     |
                       | message_content  |
                       | sent_at          |
                       | status           |
                       | retry_count      |
                       +------------------+
```

### 5.2 Tabel Utama & Kolom Kritis

#### Tabel: `websites`
| Kolom | Tipe Data | Constraint |
|---|---|---|
| `id` | UUID | PK, DEFAULT gen_random_uuid() |
| `domain` | VARCHAR(253) | NOT NULL |
| `port` | SMALLINT | NOT NULL, DEFAULT 443 |
| `owner_name` | VARCHAR(150) | NOT NULL |
| `owner_wa` | VARCHAR(20) | NOT NULL |
| `is_active` | BOOLEAN | NOT NULL, DEFAULT true |
| `created_at` | TIMESTAMPTZ | NOT NULL, DEFAULT now() |
| `created_by` | UUID | NOT NULL, FK → users.id |

**Unique Constraint:** `UNIQUE(domain, port)` — mencegah duplikasi

#### Tabel: `ssl_check_results`
| Kolom | Tipe Data | Keterangan |
|---|---|---|
| `id` | UUID | Primary key |
| `website_id` | UUID | FK → websites.id |
| `checked_at` | TIMESTAMPTZ | Waktu pemeriksaan |
| `status` | VARCHAR(20) | VALID/WARNING_30/WARNING_14/CRITICAL_7/EXPIRED/FAILED |
| `days_remaining` | INTEGER | Sisa hari sertifikat |
| `expires_at` | TIMESTAMPTZ | Tanggal kedaluwarsa |
| `fingerprint` | VARCHAR(95) | SHA-256 fingerprint |
| `sans_json` | JSONB | List Subject Alt Names |
| `chain_valid` | BOOLEAN | Validitas chain |
| `hostname_match` | BOOLEAN | Hostname cocok |

### 5.3 Indeks Database
```sql
CREATE INDEX idx_ssl_results_website_checked
  ON ssl_check_results(website_id, checked_at DESC);

CREATE INDEX idx_ssl_results_status
  ON ssl_check_results(status)
  WHERE status NOT IN ('VALID', 'FAILED');

CREATE INDEX idx_notif_logs_website_threshold
  ON notification_logs(website_id, threshold_label, sent_at DESC);

ALTER TABLE websites
  ADD CONSTRAINT uq_domain_port UNIQUE (domain, port);
```

---

## 6. KONTRAK ANTARMUKA API

### 6.1 Konvensi Umum API

```
Base URL      : https://{host}/api/v1
Content-Type  : application/json
Authorization : Bearer {jwt_access_token}

HTTP Status Codes:
  200 OK              - Request berhasil
  201 Created         - Resource berhasil dibuat
  400 Bad Request     - Validasi input gagal
  401 Unauthorized    - Token tidak valid/expired
  403 Forbidden       - Tidak punya izin
  404 Not Found       - Resource tidak ditemukan
  409 Conflict        - Duplikasi data
  429 Too Many Req    - Rate limit tercapai
  500 Internal Error  - Kesalahan server
```

### 6.2 Endpoint Utama

| Method | Endpoint | Aksi | Role |
|---|---|---|---|
| POST | /auth/login | Login, dapatkan JWT | Public |
| POST | /auth/logout | Invalidate token | All |
| GET | /websites | Daftar semua website | All |
| POST | /websites | Tambah domain baru | ADMIN+ |
| GET | /websites/{id} | Detail + histori check | All |
| PUT | /websites/{id} | Update domain | ADMIN+ |
| DELETE | /websites/{id} | Hapus domain (soft) | SUPER_ADMIN |
| POST | /websites/{id}/check | Scan manual | ADMIN+ |
| GET | /dashboard/summary | Ringkasan metrik | All |
| GET | /notifications/logs | Log pengiriman WA | All |
| POST | /notifications/test | Tes kirim WA | ADMIN+ |
| GET | /reports/export | Export CSV | All |
| GET | /users | Daftar user | SUPER_ADMIN |
| POST | /users | Tambah user | SUPER_ADMIN |

### 6.3 Contoh Response: Dashboard Summary
```json
{
  "status": "success",
  "data": {
    "total_domains": 8,
    "valid": 4,
    "warning_30": 1,
    "warning_14": 1,
    "critical_7": 1,
    "expired": 0,
    "failed": 1,
    "last_scan": "2026-10-20T07:00:00Z",
    "next_scan": "2026-10-21T07:00:00Z"
  }
}
```

---

## 7. SPESIFIKASI ANTARMUKA PENGGUNA

### 7.1 Struktur Navigasi & Sitemap

```
/login
  └── [Auth berhasil] → /app

/app (SPA — Single Page Application)
  ├── Dashboard    — Ringkasan status semua domain
  ├── Kelola Website — Daftar & manajemen domain
  │     ├── [Modal] Tambah Domain
  │     ├── [Modal] Edit Domain
  │     └── [Modal] Detail & Histori Sertifikat
  ├── Log WhatsApp — Log pengiriman notifikasi
  └── Pengguna & Role — Manajemen user (SUPER_ADMIN only)
```

### 7.2 Design Token & Sistem Warna

```css
/* Palet Utama — Neon Blue Dark Theme (sama dengan halaman login) */
--bg-darkest:    #02040A;    /* Background login & body */
--bg-main:       #050811;    /* Background dashboard */
--bg-card:       rgba(8, 14, 30, 0.80);   /* Card/panel */
--bg-sidebar:    rgba(3, 6, 16, 0.97);    /* Sidebar */
--bg-modal:      #070D1E;    /* Modal dialog */

/* Aksen Neon Biru */
--blue-neon:     #2563EB;    /* Primary action, borders */
--blue-deep:     #0066FF;    /* Gradient ujung */
--cyan-primary:  #38BDF8;    /* Highlight, link aktif */

/* Status */
--green-valid:   #10B981;    /* Sertifikat aman */
--amber-warning: #F59E0B;    /* Peringatan H-30/H-14 */
--red-critical:  #F43F5E;    /* Kritis H-7/Expired */

/* Border */
--border-subtle: rgba(37, 99, 235, 0.15);
--border-focus:  rgba(56, 189, 248, 0.50);
```

### 7.3 Spesifikasi Layar per Halaman

#### Halaman Login:
| Elemen | Spesifikasi |
|---|---|
| Background | Full-screen #02040A, neon SVG S-curve biru |
| Form Card | Glassmorphism, max-width 380px, border-radius 24px |
| Judul | "SSL GUARD", font Outfit 700, warna putih |
| Input | Pill shape (border-radius 30px) |
| Tombol Login | Full-width, background putih solid, teks hitam |

#### Halaman Dashboard:
| Elemen | Spesifikasi |
|---|---|
| Sidebar | Fixed left, lebar 260px, neon blue border |
| Metric Cards | Grid 4 kolom: Total, Valid, Warning, Kritis |
| Panel Bawah | Split 2 kolom: Domain Kritis + Aturan Threshold |
| Topbar | Sticky, judul halaman + waktu real-time + tombol aksi |

---

## 8. SPESIFIKASI NON-FUNGSIONAL

### 8.1 Kinerja (Performance)

| Parameter | Target |
|---|---|
| Waktu respons API (non-SSL check) | P95 <= 200ms |
| Waktu SSL check per domain | <= 5 detik |
| Throughput scheduler | 100 domain/menit |
| First Contentful Paint frontend | <= 1.5 detik |
| Concurrent users | 50 simultan tanpa degradasi |

### 8.2 Keamanan (Security)

| Aspek | Implementasi |
|---|---|
| Autentikasi | JWT HS256, expire 60 menit |
| Hashing Password | bcrypt, salt factor 12 |
| Anti-SSRF | Blacklist IP private sebelum koneksi ke target |
| Input Sanitization | Pydantic validation ketat pada semua input |
| SQL Injection | SQLAlchemy ORM (parameterized queries) |
| CORS | Whitelist origin eksplisit, no wildcard di production |
| Transport | HTTPS wajib TLS 1.2+ |
| Secrets | Environment variable, tidak hardcoded |

### 8.3 Keandalan (Reliability) & Skalabilitas

| Parameter | Target |
|---|---|
| Uptime sistem | >= 99.5% |
| Scheduler success rate | >= 99% |
| Data backup | Harian, retention 30 hari |
| Domain terpantau saat ini | 50 domain |
| Kapasitas target | 500+ domain |

---

## 9. ALUR LOGIKA & STATE MACHINE SISTEM

### 9.1 State Machine Sertifikat SSL

```
                    +--------------------------+
                    |        VALID             |
                    |  (days_remaining > 30)   |
                    +-----------+--------------+
                                | days <= 30
                                v
                    +--------------------------+
                    |      WARNING_30          |
                    |  (15 < days <= 30)       |--+
                    +-----------+--------------+  |
                                | days <= 14      |
                                v                 | Sertifikat
                    +--------------------------+  | diperbarui
                    |      WARNING_14          |  | (days reset)
                    |  (7 < days <= 14)        |  |
                    +-----------+--------------+  |
                                | days <= 7       |
                                v                 |
                    +--------------------------+  |
                    |       CRITICAL_7         |  |
                    |   (0 < days <= 7)        |  |
                    +-----------+--------------+  |
                                | days = 0        |
                                v                 |
                    +--------------------------+  |
                    |        EXPIRED           +--+
                    |   (days_remaining <= 0)  |
                    +--------------------------+

  FAILED: koneksi/TLS error (terpisah dari alur utama)
```

### 9.2 Alur End-to-End Harian

```
[07:00 WIB] APScheduler Trigger
     |
     v
[Ambil semua websites WHERE is_active=true]
     |
     v
[Parallel: inspect_ssl(domain, port)]
     |          |
     |  GAGAL   +---> Log FAILED, lanjut ke domain berikutnya
     |
  BERHASIL
     |
     v
[Hitung days_remaining & tentukan status]
     |
     v
[Simpan ke ssl_check_results]
     |
     v
[Evaluasi: apakah perlu notifikasi?]
     |
     +---> days > 30:         SKIP
     +---> WARNING_30/14:     Cek idempotency siklus
     |                           Belum dikirim? -> Kirim WA -> Log SENT
     |                           Sudah dikirim? -> Log SKIPPED
     +---> CRITICAL_7/EXPIRED: Kirim setiap run (tanpa cek siklus)
                                -> Kirim WA -> Log SENT/FAILED
```

---

## 10. RENCANA IMPLEMENTASI & MILESTONE

### 10.1 Roadmap Pengembangan (8 Fase)

| Fase | Nama | Durasi | Output |
|---|---|---|---|
| **0** | Persiapan | 1 minggu | Repo, env, struktur proyek |
| **1** | Backend Core | 2 minggu | API auth + CRUD website |
| **2** | SSL Engine | 1 minggu | inspect_ssl + SSRF protection |
| **3** | Scheduler & Alert | 1 minggu | Cron job + idempotency |
| **4** | Integrasi WhatsApp | 1 minggu | Notifikasi end-to-end |
| **5** | Frontend | 2 minggu | Dashboard SPA lengkap |
| **6** | Testing | 1 minggu | Unit + integration + security test |
| **7** | Deployment | 1 minggu | Nginx + Uvicorn + dokumentasi |

**Total Estimasi:** ~10 minggu (Agustus–Oktober 2026)

### 10.2 Risiko Teknis & Mitigasi

| ID | Risiko | Probabilitas | Dampak | Mitigasi |
|---|---|---|---|---|
| R01 | WhatsApp API rate limit | Sedang | Tinggi | Batching + exponential backoff |
| R02 | Domain target memblokir scanning | Sedang | Sedang | Timeout handling, log FAILED |
| R03 | Scheduler tidak berjalan (server restart) | Sedang | Tinggi | misfire_grace_time + health check |
| R04 | Token WA expired | Rendah | Tinggi | Auto-refresh + alerting admin |
| R05 | False positive karena CDN/WAF | Sedang | Sedang | Test domain known-good + logging |

---

## 11. MATRIKS KETERTELUSURAN TERPADU

| Kebutuhan Bisnis | FR ID | Komponen Teknis | Test Case ID |
|---|---|---|---|
| BR-01: Pemantauan otomatis semua domain | FR-SCH-01 | APScheduler CronTrigger | TC-SCH-001 |
| BR-02: Deteksi dini H-30 | FR-ALT-01 | alert_evaluation.py | TC-ALT-001 |
| BR-03: Deteksi dini H-14 | FR-ALT-02 | alert_evaluation.py | TC-ALT-002 |
| BR-04: Notifikasi kritis H-7 harian | FR-ALT-03 | alert_evaluation.py | TC-ALT-003 |
| BR-05: Notifikasi via WhatsApp | FR-NOT-01 | whatsapp_service.py | TC-NOT-001 |
| BR-06: Anti-spam idempotency | FR-ALT-04 | idempotency.py | TC-ALT-010 |
| BR-07: Dashboard monitoring real-time | FR-DSH-01 | frontend/dashboard.js | TC-UI-001 |
| BR-08: Manajemen domain (CRUD) | FR-WEB-01 | /api/v1/websites | TC-API-001–005 |
| BR-09: Keamanan akses (RBAC) | FR-AUTH-01 | auth_service.py | TC-SEC-001 |
| BR-10: Proteksi SSRF | FR-SEC-01 | ssrf_validator.py | TC-SEC-010 |

---

## 12. GLOSARIUM DAN REFERENSI

### Glosarium Teknis:

| Istilah | Definisi |
|---|---|
| **SSL/TLS** | Secure Sockets Layer / Transport Layer Security — protokol kriptografi untuk komunikasi aman |
| **x509** | Standar format sertifikat digital yang digunakan oleh SSL/TLS |
| **JWT** | JSON Web Token — standar token autentikasi stateless |
| **SSRF** | Server-Side Request Forgery — serangan yang memaksa server melakukan request ke target tidak sah |
| **APScheduler** | Advanced Python Scheduler — library penjadwalan task Python |
| **Idempotency** | Sifat operasi yang menghasilkan output sama meskipun dijalankan berkali-kali |
| **bcrypt** | Algoritma hashing password adaptif yang tahan brute force |
| **RBAC** | Role-Based Access Control — kontrol akses berbasis peran pengguna |
| **SAN** | Subject Alternative Names — daftar domain yang dicakup oleh satu sertifikat |
| **fingerprint** | Hash SHA-256 dari DER-encoded sertifikat untuk identifikasi unik |
| **ORM** | Object-Relational Mapper — abstraksi database dengan pendekatan OOP |
| **SPA** | Single Page Application — aplikasi web yang memuat satu halaman HTML |

### Referensi Standar:

| Dokumen | Keterangan |
|---|---|
| RFC 5246 | The TLS Protocol Version 1.2 |
| RFC 8446 | The TLS Protocol Version 1.3 |
| RFC 5280 | Internet X.509 PKI Certificate |
| RFC 7519 | JSON Web Token (JWT) |
| ISO/IEC 27001:2022 | Information Security Management |
| Peraturan BSSN | Pedoman Keamanan Sistem Elektronik Pemerintah |

### Referensi Dokumen Proyek:

| Dokumen | Nomor | Lokasi |
|---|---|---|
| Business Requirements Document | BRD-SSLGUARD-2026-001 | BRD_SSLGuard_SSL_Checker.md |
| Software Requirements Specification | SRS-SSLGUARD-2026-001 | SRS_SSLGuard_SSL_Checker.md |
| Functional Specification Document | FSD-SSLGUARD-2026-001 | FSD_SSLGuard_SSL_Checker.md |
| Rancangan Sistem | - | Rancangan_Sistem_SSLGuard_SSL_Checker.docx |

---

*Dokumen PSD ini adalah living document yang akan diperbarui seiring perkembangan implementasi. Setiap perubahan signifikan harus disetujui oleh Product Owner dan dicatat dalam riwayat versi.*

**Riwayat Perubahan:**

| Versi | Tanggal | Penyusun | Perubahan |
|---|---|---|---|
| 1.0 | Oktober 2026 | Tim PKL 2026 KOMINFO | Versi awal — rilis pertama |
