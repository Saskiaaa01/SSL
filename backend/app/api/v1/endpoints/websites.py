from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.website import Website
from app.models.ssl_check import SslCheckResult
from app.schemas.website import WebsiteOut, WebsiteCreate, WebsiteUpdate, WebsiteDetailOut
from app.schemas.ssl_check import SslCheckResultOut
from app.services.scheduler import execute_inspection_for_website

router = APIRouter()


def populate_latest_check(website: Website) -> dict:
    latest = website.ssl_checks[0] if website.ssl_checks else None
    res = {
        "id": website.id,
        "domain": website.domain,
        "port": website.port,
        "owner_name": website.owner_name,
        "owner_wa": website.owner_wa,
        "department": website.department,
        "is_active": website.is_active,
        "created_at": website.created_at,
        "updated_at": website.updated_at,
        "latest_check": latest
    }
    return res


@router.get("", response_model=List[WebsiteOut])
def list_websites(
    department: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """List all monitored websites with their latest SSL check results."""
    query = db.query(Website).filter(Website.is_active == True)

    # If owner role, scope by department
    if current_user and current_user.role == "OWNER" and current_user.department:
        query = query.filter(Website.department == current_user.department)
    elif department:
        query = query.filter(Website.department == department)

    websites = query.order_by(Website.domain.asc()).all()
    return [populate_latest_check(w) for w in websites]


@router.post("", response_model=WebsiteOut, status_code=status.HTTP_201_CREATED)
async def create_website(
    data: WebsiteCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """Register a new domain and immediately inspect its SSL certificate."""
    existing = db.query(Website).filter(
        Website.domain == data.domain,
        Website.port == data.port
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Domain {data.domain}:{data.port} sudah terdaftar dalam sistem monitoring."
        )

    website = Website(
        domain=data.domain,
        port=data.port,
        owner_name=data.owner_name,
        owner_wa=data.owner_wa,
        department=data.department,
        is_active=data.is_active,
        created_by=current_user.id if current_user else None
    )
    db.add(website)
    db.commit()
    db.refresh(website)

    # Immediately perform initial SSL inspection
    try:
        await execute_inspection_for_website(website, db)
    except Exception:
        pass

    db.refresh(website)
    return populate_latest_check(website)


@router.get("/{website_id}", response_model=WebsiteDetailOut)
def get_website_detail(website_id: str, db: Session = Depends(get_db)):
    """Retrieve full details and inspection history for a website."""
    website = db.query(Website).filter(Website.id == website_id).first()
    if not website:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Domain tidak ditemukan.")
    
    out = populate_latest_check(website)
    out["ssl_checks"] = website.ssl_checks
    return out


@router.put("/{website_id}", response_model=WebsiteOut)
def update_website(website_id: str, data: WebsiteUpdate, db: Session = Depends(get_db)):
    """Update website domain metadata."""
    website = db.query(Website).filter(Website.id == website_id).first()
    if not website:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Domain tidak ditemukan.")

    update_dict = data.model_dump(exclude_unset=True)
    for field, val in update_dict.items():
        setattr(website, field, val)

    db.commit()
    db.refresh(website)
    return populate_latest_check(website)


@router.delete("/{website_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_website(website_id: str, db: Session = Depends(get_db)):
    """Delete website domain from monitoring."""
    website = db.query(Website).filter(Website.id == website_id).first()
    if not website:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Domain tidak ditemukan.")

    db.delete(website)
    db.commit()
    return None


@router.post("/{website_id}/check", response_model=SslCheckResultOut)
async def check_website_now(website_id: str, db: Session = Depends(get_db)):
    """Trigger manual on-demand SSL inspection for a domain."""
    website = db.query(Website).filter(Website.id == website_id).first()
    if not website:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Domain tidak ditemukan.")

    result = await execute_inspection_for_website(website, db)
    return result
