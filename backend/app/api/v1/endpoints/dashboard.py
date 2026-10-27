from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.website import Website
from app.schemas.dashboard import DashboardSummary, DashboardStats
from app.api.v1.endpoints.websites import populate_latest_check
from app.services.scheduler import run_daily_monitoring_job

router = APIRouter()


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """Aggregate statistics for executive dashboard."""
    query = db.query(Website).filter(Website.is_active == True)
    if current_user and current_user.role == "OWNER" and current_user.department:
        query = query.filter(Website.department == current_user.department)

    websites = query.all()

    total = len(websites)
    valid_count = 0
    warning_30_count = 0
    warning_14_count = 0
    critical_7_count = 0
    expired_count = 0
    failed_count = 0
    urgent_list = []

    last_scan_time = None

    for w in websites:
        item = populate_latest_check(w)
        latest = item["latest_check"]
        if latest:
            if not last_scan_time or latest.checked_at > last_scan_time:
                last_scan_time = latest.checked_at

            st = latest.status
            if st == "VALID":
                valid_count += 1
            elif st == "WARNING_30":
                warning_30_count += 1
            elif st == "WARNING_14":
                warning_14_count += 1
            elif st == "CRITICAL_7":
                critical_7_count += 1
            elif st == "EXPIRED":
                expired_count += 1
            elif st == "FAILED":
                failed_count += 1

            if st in ("CRITICAL_7", "EXPIRED", "WARNING_14", "WARNING_30", "FAILED"):
                urgent_list.append(item)
        else:
            failed_count += 1
            urgent_list.append(item)

    # Sort urgent list by daysRemaining ascending (expired/critical first)
    def sort_key(x):
        chk = x.get("latest_check")
        if not chk or chk.days_remaining is None:
            return 999
        return chk.days_remaining

    urgent_list.sort(key=sort_key)

    stats = DashboardStats(
        total_domains=total,
        valid=valid_count,
        warning_30=warning_30_count,
        warning_14=warning_14_count,
        critical_7=critical_7_count,
        expired=expired_count,
        failed=failed_count,
        last_scan=last_scan_time,
        next_scan=datetime.utcnow()
    )

    return {
        "stats": stats,
        "urgent_domains": urgent_list
    }


@router.post("/scan-all")
def trigger_scan_all(background_tasks: BackgroundTasks):
    """Trigger background re-scan of all domains."""
    background_tasks.add_task(run_daily_monitoring_job)
    return {"status": "success", "message": "Proses pemindaian seluruh domain telah dimulai di latar belakang."}
