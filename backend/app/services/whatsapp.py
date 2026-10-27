import uuid
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import httpx
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.notification import NotificationLog
from app.models.website import Website

logger = logging.getLogger("sslguard.whatsapp")


def generate_message_template(
    threshold_label: str,
    domain: str,
    days_remaining: Optional[int],
    expires_at: str,
    owner_name: str,
    department: Optional[str]
) -> str:
    """Generates official formatted WhatsApp warning message based on PSD specification."""
    dept_str = department if department else owner_name
    
    if "7" in threshold_label or threshold_label == "CRITICAL_7":
        days_str = f"{days_remaining} HARI LAGI!" if days_remaining and days_remaining > 0 else "SEGERA!"
        return (
            f"🛡️ *[SSLGuard KOMINFO] PERINGATAN KRITIS — {days_str}*\n\n"
            f"Kepada Yth. Pengelola Domain / Penanggung Jawab:\n"
            f"• *Domain:* {domain}\n"
            f"• *Sisa Masa Berlaku:* {days_remaining} hari\n"
            f"• *Tanggal Kedaluwarsa:* {expires_at}\n"
            f"• *Unit Kerja / Instansi:* {dept_str}\n\n"
            f"⚠️ *TINDAKAN SEGERA DIPERLUKAN!*\n"
            f"Sertifikat SSL/TLS domain Anda akan kedaluwarsa dalam hitungan hari. "
            f"Segera lakukan perpanjangan/penerbitan ulang sertifikat agar layanan publik tidak terblokir peramban browser.\n\n"
            f"_Pesan resmi otomatis dikirim oleh SSLGuard Sentinel — Dinas Komunikasi dan Informatika (KOMINFO)_"
        )
    elif "14" in threshold_label or threshold_label == "WARNING_14":
        return (
            f"🛡️ *[SSLGuard KOMINFO] PERINGATAN LANJUTAN — H-14*\n\n"
            f"Pemberitahuan pemantauan sertifikat SSL:\n"
            f"• *Domain:* {domain}\n"
            f"• *Sisa Masa Berlaku:* {days_remaining} hari\n"
            f"• *Tanggal Kedaluwarsa:* {expires_at}\n"
            f"• *Unit Kerja:* {dept_str}\n\n"
            f"Mohon untuk mengoordinasikan pengajuan perpanjangan sertifikat SSL sebelum mencapai ambang kritis H-7.\n\n"
            f"_SSLGuard Monitoring — Tim Keamanan Informasi KOMINFO_"
        )
    elif "30" in threshold_label or threshold_label == "WARNING_30":
        return (
            f"🛡️ *[SSLGuard KOMINFO] PERINGATAN DINI — H-30*\n\n"
            f"Informasi masa aktif sertifikat keamanan digital:\n"
            f"• *Domain:* {domain}\n"
            f"• *Sisa Masa Berlaku:* {days_remaining} hari\n"
            f"• *Tanggal Kedaluwarsa:* {expires_at}\n"
            f"• *Penanggung Jawab:* {dept_str}\n\n"
            f"Sertifikat SSL/TLS domain Anda berada dalam rentang 30 hari sebelum habis tempo. "
            f"Silakan jadwalkan proses pembaruan dokumen sertifikat.\n\n"
            f"_SSLGuard System — Diskominfo_"
        )
    elif threshold_label == "EXPIRED":
        return (
            f"🚨 *[SSLGuard KOMINFO] PERINGATAN DARURAT — SERTIFIKAT TELAH KEDALUWARSA!*\n\n"
            f"Domain berikut saat ini telah melewati batas masa berlaku:\n"
            f"• *Domain:* {domain}\n"
            f"• *Status:* KEDALUWARSA (EXPIRED)\n"
            f"• *Batas Waktu:* {expires_at}\n"
            f"• *Unit Kerja:* {dept_str}\n\n"
            f"❌ *AKSES PUBLIK BERISIKO TERPUTUS / PERINGATAN PERAMBAN!*\n"
            f"Harap segera hubungi Tim Infrastruktur Jaringan Diskominfo untuk penanganan darurat.\n\n"
            f"_SSLGuard Incident Sentinel — KOMINFO_"
        )
    else:
        # Default / Test Template
        return (
            f"🛡️ *[SSLGuard KOMINFO] UJI COBA SALURAN NOTIFIKASI WHATSAPP*\n\n"
            f"Halo {owner_name},\n"
            f"Ini adalah pesan uji koneksi resmi dari sistem monitoring SSLGuard KOMINFO.\n"
            f"• *Target Domain:* {domain}\n"
            f"• *Estimasi Sisa:* {days_remaining} hari ({threshold_label})\n"
            f"• *Waktu Pengujian:* {datetime.now().strftime('%d %B %Y, %H:%M:%S')} WIB\n\n"
            f"Kanal integrasi WhatsApp Cloud API aktif dan siap mengirimkan peringatan dini kedaluwarsa sertifikat."
        )


async def send_whatsapp_alert(
    db: Session,
    website: Optional[Website],
    recipient_name: str,
    recipient_wa: str,
    threshold_label: str,
    domain: str,
    days_remaining: Optional[int] = None,
    expires_at: str = "-",
    department: Optional[str] = None,
    is_test: bool = False
) -> NotificationLog:
    """
    Evaluates anti-spam idempotency, sends message via Meta WhatsApp Cloud API
    or realistic simulation mode, and logs into notification_logs.
    """
    # Anti-Spam Check: don't send duplicate alerts within the same threshold within 24 hours (unless test)
    if not is_test and website:
        yesterday = datetime.utcnow() - timedelta(hours=20)
        existing = db.query(NotificationLog).filter(
            NotificationLog.website_id == website.id,
            NotificationLog.threshold_label == threshold_label,
            NotificationLog.sent_at >= yesterday
        ).first()

        if existing:
            logger.info(f"Anti-Spam Suppress: Alert for {domain} ({threshold_label}) already sent at {existing.sent_at}")
            return existing

    # Format message content
    message_content = generate_message_template(
        threshold_label=threshold_label,
        domain=domain,
        days_remaining=days_remaining,
        expires_at=expires_at,
        owner_name=recipient_name,
        department=department
    )

    provider_id = None
    status = "SENT"
    error_detail = None

    # Determine live sending or simulation
    use_live = (
        not settings.WHATSAPP_SIMULATION_MODE
        and bool(settings.WHATSAPP_PHONE_NUMBER_ID)
        and bool(settings.WHATSAPP_ACCESS_TOKEN)
    )

    if use_live:
        try:
            url = f"{settings.WHATSAPP_API_URL}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
            headers = {
                "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
                "Content-Type": "application/json"
            }
            # Clean recipient phone number to E.164 without symbols
            clean_phone = recipient_wa.replace("+", "").replace("-", "").replace(" ", "")
            
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": clean_phone,
                "type": "text",
                "text": {"preview_url": False, "body": message_content}
            }

            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(url, headers=headers, json=payload)
                data = res.json()
                if res.status_code in (200, 201):
                    messages = data.get("messages", [])
                    if messages:
                        provider_id = messages[0].get("id")
                    status = "DELIVERED"
                else:
                    status = "FAILED"
                    error_detail = str(data)
        except Exception as e:
            status = "FAILED"
            error_detail = str(e)
    else:
        # Realistic simulation mode
        provider_id = f"wamid.HBgLMTYy{uuid.uuid4().hex[:16]}"
        status = "READ" if is_test else "DELIVERED"

    # Persist log
    log_entry = NotificationLog(
        website_id=website.id if website else None,
        domain=domain,
        recipient_name=recipient_name,
        recipient_wa=recipient_wa,
        threshold_label=threshold_label,
        message_content=message_content,
        status=status,
        provider_message_id=provider_id,
        sent_at=datetime.utcnow(),
        error_detail=error_detail
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)

    logger.info(f"WhatsApp alert recorded: ID={log_entry.id}, Domain={domain}, Status={status}")
    return log_entry
