from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class SslCheckResultBase(BaseModel):
    status: str
    days_remaining: Optional[int] = None
    issuer: Optional[str] = None
    subject_cn: Optional[str] = None
    valid_from: Optional[str] = None
    expires_at: Optional[str] = None
    fingerprint_sha256: Optional[str] = None
    serial_number: Optional[str] = None
    key_info: Optional[str] = None
    sans: Optional[str] = None
    chain_valid: bool = True
    hostname_match: bool = True
    error_message: Optional[str] = None
    response_time_ms: Optional[int] = None


class SslCheckResultOut(SslCheckResultBase):
    id: str
    website_id: str
    checked_at: datetime

    class Config:
        from_attributes = True
