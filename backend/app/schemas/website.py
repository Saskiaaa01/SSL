from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, field_validator
import re
from app.schemas.ssl_check import SslCheckResultOut


class WebsiteBase(BaseModel):
    domain: str
    port: int = 443
    owner_name: str
    owner_wa: str
    department: Optional[str] = None
    is_active: bool = True

    @field_validator("domain")
    @classmethod
    def clean_domain(cls, v: str) -> str:
        # Strip protocol if user inputs https://domain.go.id
        v = v.strip().lower()
        v = re.sub(r"^https?://", "", v)
        v = v.split("/")[0]  # remove paths
        v = v.split(":")[0]  # remove port if present
        if not v:
            raise ValueError("Domain tidak boleh kosong")
        return v


class WebsiteCreate(WebsiteBase):
    pass


class WebsiteUpdate(BaseModel):
    domain: Optional[str] = None
    port: Optional[int] = None
    owner_name: Optional[str] = None
    owner_wa: Optional[str] = None
    department: Optional[str] = None
    is_active: Optional[bool] = None


class WebsiteOut(WebsiteBase):
    id: str
    created_at: datetime
    updated_at: datetime
    latest_check: Optional[SslCheckResultOut] = None

    class Config:
        from_attributes = True


class WebsiteDetailOut(WebsiteOut):
    ssl_checks: List[SslCheckResultOut] = []

    class Config:
        from_attributes = True
