import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class SslCheckResult(Base):
    __tablename__ = "ssl_check_results"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    website_id = Column(String(36), ForeignKey("websites.id"), nullable=False, index=True)
    checked_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Status: VALID, WARNING_30, WARNING_14, CRITICAL_7, EXPIRED, FAILED
    status = Column(String(20), nullable=False, index=True)
    days_remaining = Column(Integer, nullable=True)
    
    issuer = Column(String(255), nullable=True)
    subject_cn = Column(String(255), nullable=True)
    valid_from = Column(String(50), nullable=True)
    expires_at = Column(String(50), nullable=True)
    
    fingerprint_sha256 = Column(String(95), nullable=True)
    serial_number = Column(String(100), nullable=True)
    key_info = Column(String(100), nullable=True)
    sans = Column(Text, nullable=True)  # Comma separated or JSON string
    
    chain_valid = Column(Boolean, default=True, nullable=False)
    hostname_match = Column(Boolean, default=True, nullable=False)
    error_message = Column(Text, nullable=True)
    response_time_ms = Column(Integer, nullable=True)

    website = relationship("Website", back_populates="ssl_checks")
