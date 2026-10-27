import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class NotificationLog(Base):
    __tablename__ = "notification_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    website_id = Column(String(36), ForeignKey("websites.id"), nullable=True, index=True)
    domain = Column(String(253), nullable=False, index=True)
    recipient_name = Column(String(150), nullable=False)
    recipient_wa = Column(String(20), nullable=False)
    
    # Threshold: H-30, H-14, H-7, EXPIRED, TEST
    threshold_label = Column(String(30), nullable=False, index=True)
    message_content = Column(Text, nullable=False)
    
    # Status: SENT, DELIVERED, READ, FAILED
    status = Column(String(20), default="SENT", nullable=False)
    provider_message_id = Column(String(100), nullable=True)
    sent_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    retry_count = Column(Integer, default=0, nullable=False)
    error_detail = Column(Text, nullable=True)

    website = relationship("Website", back_populates="notification_logs")
