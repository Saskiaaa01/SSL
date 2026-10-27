from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class NotificationLogOut(BaseModel):
    id: str
    website_id: Optional[str] = None
    domain: str
    recipient_name: str
    recipient_wa: str
    threshold_label: str
    message_content: str
    status: str
    provider_message_id: Optional[str] = None
    sent_at: datetime
    error_detail: Optional[str] = None

    class Config:
        from_attributes = True


class NotificationTestRequest(BaseModel):
    phone_number: str
    recipient_name: str = "Administrator KOMINFO"
    domain: str = "portal.dinas.go.id"
    days_remaining: int = 5
    threshold_label: str = "H-7 (Kritis)"


class NotificationTestResponse(BaseModel):
    status: str
    message: str
    provider_id: Optional[str] = None
    log_id: Optional[str] = None
