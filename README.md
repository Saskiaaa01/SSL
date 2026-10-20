# SSLGuard 🛡️
### SSL/TLS Certificate Monitoring & WhatsApp Alert System

> Sistem Pemantauan Masa Berlaku Sertifikat SSL/TLS & Notifikasi Peringatan Dini WhatsApp  
> **Program Praktik Kerja Lapangan (PKL) 2026 - Dinas Komunikasi dan Informatika (KOMINFO)**

---

## 📌 Ringkasan Proyek
**SSLGuard** adalah sistem pemantauan proaktif terhadap masa berlaku dan validitas sertifikat SSL/TLS untuk seluruh portal website dan subdomain instansi pemerintah. Sistem ini secara otomatis menginspeksi sertifikat publik dan mengirimkan peringatan berjenjang via **WhatsApp** pada ambang batas **H-30, H-14, dan H-7** kepada Administrator dan Pemilik Domain (*Owner*).

---

## 📚 Dokumen Spesifikasi Rekayasa Perangkat Lunak

Repositori ini memuat dokumen perancangan dan spesifikasi lengkap:

| Dokumen | Berkas | Deskripsi Singkat |
| :--- | :--- | :--- |
| **BRD** | [BRD_SSLGuard_SSL_Checker.md](BRD_SSLGuard_SSL_Checker.md) | **Business Requirements Document:** Latar belakang masalah, analisis stakeholder, BPMN alur bisnis, KPI, dan aturan bisnis. |
| **SRS** | [SRS_SSLGuard_SSL_Checker.md](SRS_SSLGuard_SSL_Checker.md) | **Software Requirements Specification:** Kebutuhan fungsional (FR-01 s.d. FR-07), non-fungsional, arsitektur, ERD, dan use case. |
| **FSD** | [FSD_SSLGuard_SSL_Checker.md](FSD_SSLGuard_SSL_Checker.md) | **Functional Specification Document:** Wireframe antarmuka, spesifikasi use case klik-demi-klik, kontrak API payload JSON, dan pseudocode algoritma. |
| **Rancangan Teknis** | `Rancangan_Sistem_SSLGuard_SSL_Checker.docx` | Dokumen rancangan awal arsitektur dan basis data. |

---

## 🚀 Fitur Utama
1. **SSL/TLS Inspection Engine:** Mengambil sertifikat publik x509 via TLS Handshake, mengekstrak masa berlaku, penerbit (CA), kecocokan hostname, dan sidik jari SHA-256.
2. **Scheduled Daily Monitoring:** Penjadwalan harian otomatis berbasis APScheduler untuk memeriksa seluruh domain aktif.
3. **WhatsApp Multi-Threshold Notification:** Pengiriman notifikasi ke WhatsApp Admin & Pemilik Domain pada H-30, H-14, dan H-7.
4. **Anti-Spam & Deduplication:** Memastikan tidak ada pesan ganda terkirim untuk siklus sertifikat dan ambang yang sama.
5. **Proteksi SSRF:** Validasi ketat nama domain guna memblokir akses ke alamat IP privat/loopback.
6. **Executive Dashboard & Audit Log:** Tampilan statistik status, riwayat inspeksi, log pengiriman WhatsApp, dan ekspor laporan ke CSV.

---

## 🛠️ Tech Stack yang Direncanakan
- **Backend:** Python + FastAPI (Uvicorn ASGI)
- **Database:** PostgreSQL (SQLAlchemy ORM + Alembic Migration)
- **Cryptography:** Python `ssl`, `socket`, `cryptography`
- **Scheduler:** APScheduler
- **Notification:** WhatsApp Business Platform / Cloud API
- **Frontend:** Modern Web Dashboard (HTML5, Vanilla CSS, JavaScript / React)

---

## 📄 Lisensi
Hak Cipta © 2026 Tim PKL KOMINFO. Seluruh hak cipta dilindungi undang-undang.
