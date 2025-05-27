# app/models/notification.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.utils.database import Base

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(200))
    message = Column(Text)
    notification_type = Column(String(50))  # message, mention, quiz, announcement, room_invite
    related_id = Column(Integer)  # ID of related entity (message, quiz, etc.)
    related_type = Column(String(50))  # type of related entity
    is_read = Column(Boolean, default=False)
    priority = Column(String(20), default="normal")  # low, normal, high, urgent
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="notifications")
