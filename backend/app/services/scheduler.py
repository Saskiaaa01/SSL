import logging
import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import SessionLocal
from app.models.website import Website
from app.models.ssl_check import SslCheckResult
from app.services.ssl_checker import inspect_ssl_certificate
from app.services.whatsapp import send_whatsapp_alert

logger = logging.getLogger("sslguard.scheduler")
scheduler = AsyncIOScheduler(timezone=settings.TIMEZONE)


async def execute_inspection_for_website(website: Website, db: Session) -> SslCheckResult:
    """Inspects a single website SSL cert, records result, and triggers alerts if required."""
    logger.info(f"Scanning domain: {website.domain}:{website.port}")
    
    # Run synchronous SSL socket inspection in thread pool
    check_data = await asyncio.to_thread(inspect_ssl_certificate, website.domain, website.port)

    # Save check result
    result = SslCheckResult(
        website_id=website.id,
        checked_at=datetime.utcnow(),
        status=check_data["status"],
        days_remaining=check_data["days_remaining"],
        issuer=check_data["issuer"],
        subject_cn=check_data["subject_cn"],
        valid_from=check_data["valid_from"],
        expires_at=check_data["expires_at"],
        fingerprint_sha256=check_data["fingerprint_sha256"],
        serial_number=check_data["serial_number"],
        key_info=check_data["key_info"],
        sans=check_data["sans"],
        chain_valid=check_data["chain_valid"],
        hostname_match=check_data["hostname_match"],
        error_message=check_data["error_message"],
        response_time_ms=check_data["response_time_ms"],
    )
    db.add(result)
    db.commit()
    db.refresh(result)

    # Threshold alerts evaluation
    status = check_data["status"]
    days = check_data["days_remaining"]
    expires_at = check_data["expires_at"]

    if status in ("CRITICAL_7", "WARNING_14", "WARNING_30", "EXPIRED"):
        threshold_map = {
            "CRITICAL_7": f"H-7 (Kritis: {days} Hari)",
            "WARNING_14": "H-14 (Lanjutan)",
            "WARNING_30": "H-30 (Awal)",
            "EXPIRED": "EXPIRED (Kedaluwarsa)"
        }
        threshold_label = threshold_map.get(status, status)

        # 1. Alert to Owner
        if website.owner_wa:
            await send_whatsapp_alert(
                db=db,
                website=website,
                recipient_name=f"{website.owner_name} (Owner)",
                recipient_wa=website.owner_wa,
                threshold_label=threshold_label,
                domain=website.domain,
                days_remaining=days,
                expires_at=expires_at,
                department=website.department
            )

        # 2. Alert to Central Admin KOMINFO
        if settings.WHATSAPP_ADMIN_PHONE:
            await send_whatsapp_alert(
                db=db,
                website=website,
                recipient_name="Administrator Pusat KOMINFO",
                recipient_wa=settings.WHATSAPP_ADMIN_PHONE,
                threshold_label=threshold_label,
                domain=website.domain,
                days_remaining=days,
                expires_at=expires_at,
                department=website.department
            )

    return result


async def run_daily_monitoring_job():
    """Daily routine executed at 07:00 WIB across all active registered domains."""
    logger.info("Executing scheduled SSL monitoring cycle across all registered domains...")
    db: Session = SessionLocal()
    try:
        websites = db.query(Website).filter(Website.is_active == True).all()
        for w in websites:
            try:
                await execute_inspection_for_website(w, db)
            except Exception as e:
                logger.error(f"Error inspecting {w.domain}: {e}")
        logger.info(f"Daily monitoring completed for {len(websites)} domains.")
    finally:
        db.close()


def start_scheduler():
    """Initializes and activates APScheduler job."""
    if not settings.SCHEDULER_ENABLED:
        logger.info("Scheduler is disabled in configuration.")
        return

    scheduler.add_job(
        func=run_daily_monitoring_job,
        trigger=CronTrigger(
            hour=settings.SCHEDULER_CRON_HOUR,
            minute=settings.SCHEDULER_CRON_MINUTE,
            timezone=settings.TIMEZONE
        ),
        id="ssl_daily_monitor",
        name="Pemindaian Rutin Harian SSLGuard (07:00 WIB)",
        replace_existing=True,
        misfire_grace_time=3600
    )
    scheduler.start()
    logger.info(f"Scheduler started. Daily run scheduled at {settings.SCHEDULER_CRON_HOUR:02d}:{settings.SCHEDULER_CRON_MINUTE:02d} {settings.TIMEZONE}")


def stop_scheduler():
    """Shuts down scheduler gracefully."""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Scheduler shutdown.")
