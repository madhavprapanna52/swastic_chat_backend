# app/services/auth_service.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import UserCreate, UserLogin
from app.utils.security import (
    get_password_hash, 
    verify_password, 
    create_access_token,
    generate_verification_token,
    extract_university_info
)
from app.services.email_service import send_verification_email
from typing import Optional
import re

class AuthService:
    
    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> dict:
        """Register a new user with university email verification"""
        
        # Validate university email
        if not AuthService.is_university_email(user_data.email):
            raise ValueError("Please use a valid university email address")
        
        # Check if username already exists
        if db.query(User).filter(User.username == user_data.username).first():
            raise ValueError("Username already taken")
        
        # Check if email already exists
        if db.query(User).filter(User.email == user_data.email).first():
            raise ValueError("Email already registered")
        
        # Extract university information
        university_domain, university_badge = extract_university_info(user_data.email)
        
        # Generate verification token
        verification_token = generate_verification_token()
        
        # Create new user
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=get_password_hash(user_data.password),
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            university_domain=university_domain,
            university_badge=university_badge,
            verification_token=verification_token,
            is_verified=False
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Send verification email
        email_sent = send_verification_email(
            user_data.email, 
            user_data.first_name, 
            verification_token
        )
        
        return {
            "user_id": new_user.id,
            "message": "Registration successful! Please check your email to verify your account.",
            "verification_required": True,
            "email_sent": email_sent
        }
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        """Authenticate user login"""
        user = db.query(User).filter(User.username == username).first()
        
        if not user:
            return None
        
        if not verify_password(password, user.password_hash):
            return None
        
        if not user.is_verified:
            raise ValueError("Please verify your email before logging in")
        
        if not user.is_active:
            raise ValueError("Account is deactivated")
        
        # Update last seen
        from datetime import datetime
        user.last_seen = datetime.utcnow()
        db.commit()
        
        return user
    
    @staticmethod
    def verify_email(db: Session, token: str) -> dict:
        """Verify user email with token"""
        user = db.query(User).filter(User.verification_token == token).first()
        
        if not user:
            raise ValueError("Invalid verification token")
        
        if user.is_verified:
            raise ValueError("Email already verified")
        
        # Verify the user
        user.is_verified = True
        user.verification_token = None
        db.commit()
        
        return {
            "message": "Email verified successfully! You can now log in.",
            "user_id": user.id
        }
    
    @staticmethod
    def is_university_email(email: str) -> bool:
        """Check if email is from a recognized university domain"""
        university_domains = [
            'edu', 'ac.in', 'edu.in', 'ernet.in',
            'iitd.ac.in', 'iitb.ac.in', 'iisc.ac.in',
            'du.ac.in', 'jnu.ac.in', 'bhu.ac.in'
            # Add more university domains as needed
        ]
        
        domain = email.split('@')[1].lower()
        return any(domain.endswith(uni_domain) for uni_domain in university_domains)
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """Get user by username"""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
