"""
Database Seeder for SSLGuard
Populates initial KOMINFO administrative users, domain inventory,
and initial audit notification logs according to the PSD specification.
"""
import uuid
from datetime import datetime, timedelta
from app.core.database import Base, engine, SessionLocal
from app.core.security import get_password_hash
from app.models.user import User
from app.models.website import Website
from app.models.ssl_check import SslCheckResult
from app.models.notification import NotificationLog


def seed():
    print("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if already seeded
        if db.query(User).first():
            print("Database already contains data. Skipping seeder.")
            return

        print("Seeding administrative and owner users...")
        users_data = [
            {
                "id": "u1",
                "username": "admin",
                "email": "admin@kominfo.go.id",
                "password_hash": get_password_hash("Admin@2026"),
                "full_name": "Admin KOMINFO",
                "role": "SUPER_ADMIN",
                "department": None,
                "phone_number": "+6281198765432",
                "is_active": True
            },
            {
                "id": "u2",
                "username": "budi",
                "email": "budi@dinas.go.id",
                "password_hash": get_password_hash("Budi@2026"),
                "full_name": "Budi Santoso",
                "role": "OWNER",
                "department": "Diskominfo",
                "phone_number": "+6281234567890",
                "is_active": True
            },
            {
                "id": "u3",
                "username": "siti",
                "email": "siti@hukum.kota.go.id",
                "password_hash": get_password_hash("Siti@2026"),
                "full_name": "Siti Rahma",
                "role": "OWNER",
                "department": "Bagian Hukum",
                "phone_number": "+6281345678901",
                "is_active": True
            },
            {
                "id": "u4",
                "username": "agus",
                "email": "agus@bkpsdm.kab.go.id",
                "password_hash": get_password_hash("Agus@2026"),
                "full_name": "Agus Pratama",
                "role": "OWNER",
                "department": "BKPSDM",
                "phone_number": "+6281987654321",
                "is_active": True
            }
        ]

        for u_data in users_data:
            user = User(**u_data)
            db.add(user)
        db.commit()

        print("Seeding official KOMINFO public domain inventory...")
        now = datetime.utcnow()
        websites_data = [
            {
                "id": "w1",
                "domain": "portal.dinas.go.id",
                "port": 443,
                "owner_name": "Budi Santoso",
                "owner_wa": "+6281234567890",
                "department": "Diskominfo",
                "is_active": True,
                "created_by": "u1",
                "check": {
                    "status": "CRITICAL_7",
                    "days_remaining": 3,
                    "issuer": "Let's Encrypt Authority R3",
                    "subject_cn": "*.dinas.go.id",
                    "valid_from": (now - timedelta(days=87)).strftime("%Y-%m-%d"),
                    "expires_at": (now + timedelta(days=3)).strftime("%Y-%m-%d"),
                    "fingerprint_sha256": "8C:64:1D:4B:92:07:95:EA:3A:41:8F:D2:C3:48:9A:F0:22:15:37:EB",
                    "serial_number": "04:3a:9e:12:87:6b:15:c2",
                    "key_info": "RSA 2048 bit (SHA256withRSA)",
                    "sans": "portal.dinas.go.id, *.dinas.go.id, dinas.go.id",
                    "chain_valid": True,
                    "hostname_match": True,
                    "error_message": None,
                    "response_time_ms": 142
                }
            },
            {
                "id": "w2",
                "domain": "jdih.kota.go.id",
                "port": 443,
                "owner_name": "Siti Rahma",
                "owner_wa": "+6281345678901",
                "department": "Bagian Hukum",
                "is_active": True,
                "created_by": "u1",
                "check": {
                    "status": "WARNING_14",
                    "days_remaining": 12,
                    "issuer": "Google Trust Services LLC",
                    "subject_cn": "jdih.kota.go.id",
                    "valid_from": (now - timedelta(days=78)).strftime("%Y-%m-%d"),
                    "expires_at": (now + timedelta(days=12)).strftime("%Y-%m-%d"),
                    "fingerprint_sha256": "3A:9F:88:C1:44:B0:18:22:90:5E:AA:77:23:44:11:09:BB:66:77:88",
                    "serial_number": "12:bb:44:aa:66:cc:01:89",
                    "key_info": "ECDSA 256 bit (SHA256withECDSA)",
                    "sans": "jdih.kota.go.id, hukum.kota.go.id",
                    "chain_valid": True,
                    "hostname_match": True,
                    "error_message": None,
                    "response_time_ms": 115
                }
            },
            {
                "id": "w3",
                "domain": "bkpsdm.kab.go.id",
                "port": 443,
                "owner_name": "Agus Pratama",
                "owner_wa": "+6281987654321",
                "department": "BKPSDM",
                "is_active": True,
                "created_by": "u1",
                "check": {
                    "status": "WARNING_30",
                    "days_remaining": 25,
                    "issuer": "Sectigo RSA Domain Validation Secure Server CA",
                    "subject_cn": "bkpsdm.kab.go.id",
                    "valid_from": (now - timedelta(days=340)).strftime("%Y-%m-%d"),
                    "expires_at": (now + timedelta(days=25)).strftime("%Y-%m-%d"),
                    "fingerprint_sha256": "5B:44:99:11:AA:FF:EE:88:22:66:11:99:33:44:55:66:77:88:99:00",
                    "serial_number": "55:88:99:aa:bb:cc:dd:ee",
                    "key_info": "RSA 2048 bit (SHA256withRSA)",
                    "sans": "bkpsdm.kab.go.id, simpeg.kab.go.id",
                    "chain_valid": True,
                    "hostname_match": True,
                    "error_message": None,
                    "response_time_ms": 188
                }
            },
            {
                "id": "w4",
                "domain": "dinkes.kotakab.go.id",
                "port": 443,
                "owner_name": "dr. Hendra Pratama",
                "owner_wa": "+6281298765432",
                "department": "Dinas Kesehatan",
                "is_active": True,
                "created_by": "u1",
                "check": {
                    "status": "VALID",
                    "days_remaining": 185,
                    "issuer": "DigiCert Global Root G2",
                    "subject_cn": "*.kotakab.go.id",
                    "valid_from": (now - timedelta(days=180)).strftime("%Y-%m-%d"),
                    "expires_at": (now + timedelta(days=185)).strftime("%Y-%m-%d"),
                    "fingerprint_sha256": "99:AA:BB:CC:DD:EE:FF:00:11:22:33:44:55:66:77:88:99:AA:BB:CC",
                    "serial_number": "09:11:22:33:44:55:66:77",
                    "key_info": "RSA 2048 bit (SHA256withRSA)",
                    "sans": "dinkes.kotakab.go.id, *.kotakab.go.id",
                    "chain_valid": True,
                    "hostname_match": True,
                    "error_message": None,
                    "response_time_ms": 94
                }
            },
            {
                "id": "w5",
                "domain": "dispendukcapil.kab.go.id",
                "port": 443,
                "owner_name": "Rian Hidayat",
                "owner_wa": "+6281399887766",
                "department": "Dispendukcapil",
                "is_active": True,
                "created_by": "u1",
                "check": {
                    "status": "VALID",
                    "days_remaining": 92,
                    "issuer": "Let's Encrypt Authority R3",
                    "subject_cn": "dispendukcapil.kab.go.id",
                    "valid_from": (now - timedelta(days=273)).strftime("%Y-%m-%d"),
                    "expires_at": (now + timedelta(days=92)).strftime("%Y-%m-%d"),
                    "fingerprint_sha256": "11:22:33:44:55:66:77:88:99:00:AA:BB:CC:DD:EE:FF:11:22:33:44",
                    "serial_number": "44:55:66:77:88:99:aa:bb",
                    "key_info": "RSA 2048 bit (SHA256withRSA)",
                    "sans": "dispendukcapil.kab.go.id, kependudukan.kab.go.id",
                    "chain_valid": True,
                    "hostname_match": True,
                    "error_message": None,
                    "response_time_ms": 130
                }
            },
            {
                "id": "w6",
                "domain": "kecamatan-barat.kab.go.id",
                "port": 443,
                "owner_name": "Dewi Lestari",
                "owner_wa": "+6281277665544",
                "department": "Kecamatan Kota",
                "is_active": True,
                "created_by": "u1",
                "check": {
                    "status": "VALID",
                    "days_remaining": 64,
                    "issuer": "ZeroSSL RSA Domain Secure CA",
                    "subject_cn": "kecamatan-barat.kab.go.id",
                    "valid_from": (now - timedelta(days=26)).strftime("%Y-%m-%d"),
                    "expires_at": (now + timedelta(days=64)).strftime("%Y-%m-%d"),
                    "fingerprint_sha256": "FF:EE:DD:CC:BB:AA:00:99:88:77:66:55:44:33:22:11:00:AA:BB:CC",
                    "serial_number": "77:88:99:aa:bb:cc:dd:11",
                    "key_info": "RSA 2048 bit (SHA256withRSA)",
                    "sans": "kecamatan-barat.kab.go.id",
                    "chain_valid": True,
                    "hostname_match": True,
                    "error_message": None,
                    "response_time_ms": 162
                }
            },
            {
                "id": "w7",
                "domain": "rsud.kotakab.go.id",
                "port": 443,
                "owner_name": "Bag. IT RSUD",
                "owner_wa": "+6281122334455",
                "department": "Dinas Kesehatan",
                "is_active": True,
                "created_by": "u1",
                "check": {
                    "status": "EXPIRED",
                    "days_remaining": -4,
                    "issuer": "Let's Encrypt Authority R3",
                    "subject_cn": "rsud.kotakab.go.id",
                    "valid_from": (now - timedelta(days=94)).strftime("%Y-%m-%d"),
                    "expires_at": (now - timedelta(days=4)).strftime("%Y-%m-%d"),
                    "fingerprint_sha256": "EE:AA:77:11:44:99:22:55:88:33:11:00:BB:CC:DD:EE:FF:11:22:33",
                    "serial_number": "99:11:aa:22:bb:33:cc:44",
                    "key_info": "RSA 2048 bit (SHA256withRSA)",
                    "sans": "rsud.kotakab.go.id",
                    "chain_valid": False,
                    "hostname_match": True,
                    "error_message": "Sertifikat telah melewati masa berlaku (Expired).",
                    "response_time_ms": 110
                }
            },
            {
                "id": "w8",
                "domain": "internal.layanan.kominfo.go.id",
                "port": 443,
                "owner_name": "Tim NOC Diskominfo",
                "owner_wa": "+6281198765432",
                "department": "Diskominfo",
                "is_active": True,
                "created_by": "u1",
                "check": {
                    "status": "FAILED",
                    "days_remaining": None,
                    "issuer": "Tidak Diketahui",
                    "subject_cn": "internal.layanan.kominfo.go.id",
                    "valid_from": "-",
                    "expires_at": "-",
                    "fingerprint_sha256": "-",
                    "serial_number": "-",
                    "key_info": "-",
                    "sans": "-",
                    "chain_valid": False,
                    "hostname_match": False,
                    "error_message": "Batas waktu koneksi habis (Connection Timeout) pada port 443.",
                    "response_time_ms": 5000
                }
            }
        ]

        for w_data in websites_data:
            check_data = w_data.pop("check")
            website = Website(**w_data)
            db.add(website)
            db.commit()

            check = SslCheckResult(
                website_id=website.id,
                checked_at=now - timedelta(minutes=15),
                **check_data
            )
            db.add(check)
        db.commit()

        print("Seeding initial WhatsApp notification audit logs...")
        notif_logs = [
            {
                "website_id": "w1",
                "domain": "portal.dinas.go.id",
                "recipient_name": "Budi Santoso (Owner Diskominfo)",
                "recipient_wa": "+6281234567890",
                "threshold_label": "H-7 (Kritis)",
                "message_content": "[SSLGuard KOMINFO] PERINGATAN KRITIS — 3 HARI LAGI!\n\nDomain: portal.dinas.go.id",
                "status": "READ",
                "provider_message_id": "wamid.HBgLMTYyODExMjM0NTZBQ",
                "sent_at": now - timedelta(hours=3, minutes=12)
            },
            {
                "website_id": "w1",
                "domain": "portal.dinas.go.id",
                "recipient_name": "Admin KOMINFO (Pengawas Pusat)",
                "recipient_wa": "+6281198765432",
                "threshold_label": "H-7 (Kritis)",
                "message_content": "[SSLGuard KOMINFO] PERINGATAN KRITIS — 3 HARI LAGI!\n\nDomain: portal.dinas.go.id",
                "status": "DELIVERED",
                "provider_message_id": "wamid.HBgLMTYyODIyMzQ1NkJB",
                "sent_at": now - timedelta(hours=3, minutes=11)
            },
            {
                "website_id": "w2",
                "domain": "jdih.kota.go.id",
                "recipient_name": "Siti Rahma (Owner Bagian Hukum)",
                "recipient_wa": "+6281345678901",
                "threshold_label": "H-14 (Lanjutan)",
                "message_content": "[SSLGuard KOMINFO] PERINGATAN LANJUTAN — H-14\n\nDomain: jdih.kota.go.id",
                "status": "DELIVERED",
                "provider_message_id": "wamid.HBgLMTYyODMzNDU2Q0E",
                "sent_at": now - timedelta(hours=5, minutes=20)
            },
            {
                "website_id": "w3",
                "domain": "bkpsdm.kab.go.id",
                "recipient_name": "Agus Pratama (Owner BKPSDM)",
                "recipient_wa": "+6281987654321",
                "threshold_label": "H-30 (Awal)",
                "message_content": "[SSLGuard KOMINFO] PERINGATAN DINI — H-30\n\nDomain: bkpsdm.kab.go.id",
                "status": "READ",
                "provider_message_id": "wamid.HBgLMTYyODQ0NTY3REE",
                "sent_at": now - timedelta(hours=8, minutes=45)
            }
        ]

        for n_data in notif_logs:
            log = NotificationLog(**n_data)
            db.add(log)
        db.commit()

        print("Database successfully seeded with realistic KOMINFO domain data!")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
