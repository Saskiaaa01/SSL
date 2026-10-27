from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from app.schemas.website import WebsiteOut


class DashboardStats(BaseModel):
    total_domains: int
    valid: int
    warning_30: int
    warning_14: int
    critical_7: int
    expired: int
    failed: int
    last_scan: Optional[datetime] = None
    next_scan: Optional[datetime] = None


class DashboardSummary(BaseModel):
    stats: DashboardStats
    urgent_domains: List[WebsiteOut] = []
