from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, require_admin
from app.models.user import User
from app.models.website import Website
from app.schemas.user import UserOut, UserCreate, UserUpdate
from app.core.security import get_password_hash

router = APIRouter()


@router.get("", response_model=List[dict])
def list_users(db: Session = Depends(get_db)):
    """List system users along with assigned domain counts."""
    users = db.query(User).order_by(User.full_name.asc()).all()
    results = []
    for u in users:
        # Count domains managed
        count_str = "Semua Domain" if u.role in ("SUPER_ADMIN", "ADMIN") else "0 Domain"
        if u.department:
            domain_count = db.query(Website).filter(Website.department == u.department).count()
            count_str = f"{domain_count} Domain ({u.department})"
        
        results.append({
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "full_name": u.full_name,
            "role": u.role,
            "department": u.department,
            "phone_number": u.phone_number,
            "is_active": u.is_active,
            "created_at": u.created_at,
            "last_login": u.last_login,
            "domains_count": count_str
        })
    return results


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    """Create a new user account."""
    existing = db.query(User).filter(
        (User.username == data.username) | (User.email == data.email)
    ).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username atau email sudah digunakan.")

    user = User(
        username=data.username,
        email=data.email,
        password_hash=get_password_hash(data.password),
        full_name=data.full_name,
        role=data.role,
        department=data.department,
        phone_number=data.phone_number,
        is_active=data.is_active
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: str, data: UserUpdate, db: Session = Depends(get_db)):
    """Update user information."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pengguna tidak ditemukan.")

    update_data = data.model_dump(exclude_unset=True)
    if "password" in update_data and update_data["password"]:
        user.password_hash = get_password_hash(update_data.pop("password"))

    for field, val in update_data.items():
        setattr(user, field, val)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    """Delete a user account."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pengguna tidak ditemukan.")

    db.delete(user)
    db.commit()
    return None
