import io
import csv
from datetime import datetime
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.website import Website

router = APIRouter()


@router.get("/export")
def export_csv_report(db: Session = Depends(get_db)):
    """Export complete SSL monitoring audit report as CSV with UTF-8 BOM."""
    websites = db.query(Website).filter(Website.is_active == True).order_by(Website.domain.asc()).all()

    output = io.StringIO()
    # Write UTF-8 BOM for Microsoft Excel compatibility
    output.write('\ufeff')
    writer = csv.writer(output, delimiter=';')

    # Header
    writer.writerow([
        "No",
        "Nama Domain",
        "Port",
        "Unit Kerja / Pemilik",
        "Nomor WhatsApp Owner",
        "Status SSL/TLS",
        "Sisa Masa Berlaku (Hari)",
        "Tanggal Berlaku",
        "Tanggal Kedaluwarsa",
        "Otoritas Penerbit (CA)",
        "Subject Common Name (CN)",
        "Sidik Jari SHA-256",
        "Pemeriksaan Terakhir"
    ])

    for idx, w in enumerate(websites, 1):
        latest = w.ssl_checks[0] if w.ssl_checks else None
        status = latest.status if latest else "BELUM_DIPERIKSA"
        days = str(latest.days_remaining) if latest and latest.days_remaining is not None else "-"
        valid_from = latest.valid_from if latest else "-"
        expires_at = latest.expires_at if latest else "-"
        issuer = latest.issuer if latest else "-"
        cn = latest.subject_cn if latest else "-"
        fingerprint = latest.fingerprint_sha256 if latest else "-"
        checked_at = latest.checked_at.strftime("%Y-%m-%d %H:%M:%S") if latest else "-"

        writer.writerow([
            idx,
            w.domain,
            w.port,
            w.department or w.owner_name,
            w.owner_wa,
            status,
            days,
            valid_from,
            expires_at,
            issuer,
            cn,
            fingerprint,
            checked_at
        ])

    output.seek(0)
    filename = f"laporan_monitoring_sslguard_kominfo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
