from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.notification import NotificationLog
from app.models.website import Website
from app.schemas.notification import NotificationLogOut, NotificationTestRequest, NotificationTestResponse
from app.services.whatsapp import send_whatsapp_alert

router = APIRouter()


@router.get("/logs", response_model=List[NotificationLogOut])
def get_notification_logs(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """Retrieve audit history of sent WhatsApp notifications."""
    query = db.query(NotificationLog).order_by(NotificationLog.sent_at.desc())
    logs = query.limit(limit).all()
    return logs


@router.post("/test", response_model=NotificationTestResponse)
async def test_send_whatsapp(data: NotificationTestRequest, db: Session = Depends(get_db)):
    """Send test notification via WhatsApp Cloud API / Simulation."""
    if not data.phone_number:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nomor WhatsApp penerima wajib diisi.")

    # Find website if exists
    website = db.query(Website).filter(Website.domain == data.domain).first()

    log_entry = await send_whatsapp_alert(
        db=db,
        website=website,
        recipient_name=data.recipient_name,
        recipient_wa=data.phone_number,
        threshold_label=data.threshold_label,
        domain=data.domain,
        days_remaining=data.days_remaining,
        expires_at="2026-11-23",
        is_test=True
    )

    return {
        "status": "success",
        "message": f"Pesan uji coba WhatsApp berhasil dikirimkan ke {data.phone_number}.",
        "provider_id": log_entry.provider_message_id,
        "log_id": log_entry.id
    }
