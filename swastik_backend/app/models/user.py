# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.utils.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    university_domain = Column(String(100), nullable=False)
    university_badge = Column(String(100), nullable=False)
    profile_picture_url = Column(String(255))
    bio = Column(Text)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String(255))
    is_active = Column(Boolean, default=True)
    last_seen = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    messages = relationship("Message", back_populates="author")
    room_memberships = relationship("RoomMember", back_populates="user")
    created_rooms = relationship("Room", back_populates="creator")
    notifications = relationship("Notification", back_populates="user")
    quiz_attempts = relationship("QuizAttempt", back_populates="user")
