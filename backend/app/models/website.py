import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base


class Website(Base):
    __tablename__ = "websites"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    domain = Column(String(253), nullable=False, index=True)
    port = Column(Integer, default=443, nullable=False)
    owner_name = Column(String(150), nullable=False)
    owner_wa = Column(String(20), nullable=False)
    department = Column(String(100), nullable=True)  # Diskominfo, Bagian Hukum, dsb.
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=True)

    __table_args__ = (
        UniqueConstraint("domain", "port", name="uq_website_domain_port"),
    )

    # Relationships
    ssl_checks = relationship("SslCheckResult", back_populates="website", cascade="all, delete-orphan", order_by="desc(SslCheckResult.checked_at)")
    notification_logs = relationship("NotificationLog", back_populates="website", cascade="all, delete-orphan")
