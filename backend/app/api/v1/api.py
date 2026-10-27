from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    websites,
    dashboard,
    notifications,
    users,
    reports
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Autentikasi & Sesi"])
api_router.include_router(websites.router, prefix="/websites", tags=["Monitoring & Kelola Website"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Executive Dashboard"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["WhatsApp Alert & Audit Log"])
api_router.include_router(users.router, prefix="/users", tags=["Manajemen Pengguna & Role"])
api_router.include_router(reports.router, prefix="/reports", tags=["Laporan Audit"])
