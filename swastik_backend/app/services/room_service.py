# app/services/room_service.py
from sqlalchemy.orm import Session
from app.models.room import Room, RoomMember
from app.models.user import User
from app.schemas.room import RoomCreate, RoomUpdate
from typing import List, Optional

class RoomService:
    
    @staticmethod
    def create_room(db: Session, room_data: RoomCreate, creator_id: int) -> Room:
        """Create a new chat room"""
        
        # Get creator info for university domain
        creator = db.query(User).filter(User.id == creator_id).first()
        if not creator:
            raise ValueError("Creator not found")
        
        # Create room
        new_room = Room(
            name=room_data.name,
            description=room_data.description,
            room_type=room_data.room_type,
            subject=room_data.subject,
            university_domain=creator.university_domain,
            max_members=room_data.max_members or 100,
            created_by=creator_id
        )
        
        db.add(new_room)
        db.commit()
        db.refresh(new_room)
        
        # Add creator as admin
        creator_membership = RoomMember(
            room_id=new_room.id,
            user_id=creator_id,
            role="admin"
        )
        
        db.add(creator_membership)
        db.commit()
        
        return new_room
    
    @staticmethod
    def join_room(db: Session, room_id: int, user_id: int) -> dict:
        """Join a user to a room"""
        
        # Check if room exists
        room = db.query(Room).filter(Room.id == room_id).first()
        if not room:
            raise ValueError("Room not found")
        
        # Check if user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        # Check if already a member
        existing_membership = db.query(RoomMember).filter(
            RoomMember.room_id == room_id,
            RoomMember.user_id == user_id
        ).first()
        
        if existing_membership:
            raise ValueError("Already a member of this room")
        
        # Check university domain for restricted rooms
        if room.university_domain and room.university_domain != user.university_domain:
            raise ValueError("This room is restricted to your university")
        
        # Check room capacity
        current_members = db.query(RoomMember).filter(RoomMember.room_id == room_id).count()
        if current_members >= room.max_members:
            raise ValueError("Room is at maximum capacity")
        
        # Add user to room
        new_membership = RoomMember(
            room_id=room_id,
            user_id=user_id,
            role="member"
        )
        
        db.add(new_membership)
        db.commit()
        
        return {
            "message": f"Successfully joined {room.name}",
            "room_id": room_id,
            "role": "member"
        }
    
    @staticmethod
    def get_user_rooms(db: Session, user_id: int) -> List[Room]:
        """Get all rooms a user is a member of"""
        
        room_memberships = db.query(RoomMember).filter(RoomMember.user_id == user_id).all()
        room_ids = [membership.room_id for membership in room_memberships]
        
        return db.query(Room).filter(Room.id.in_(room_ids), Room.is_active == True).all()
    
    @staticmethod
    def get_public_rooms(db: Session, university_domain: str = None) -> List[Room]:
        """Get public rooms, optionally filtered by university"""
        
        query = db.query(Room).filter(
            Room.room_type == "public",
            Room.is_active == True
        )
        
        if university_domain:
            query = query.filter(
                (Room.university_domain == university_domain) | 
                (Room.university_domain.is_(None))
            )
        
        return query.all()
    
    @staticmethod
    def leave_room(db: Session, room_id: int, user_id: int) -> dict:
        """Remove user from room"""
        
        membership = db.query(RoomMember).filter(
            RoomMember.room_id == room_id,
            RoomMember.user_id == user_id
        ).first()
        
        if not membership:
            raise ValueError("Not a member of this room")
        
        # Check if user is the only admin
        if membership.role == "admin":
            admin_count = db.query(RoomMember).filter(
                RoomMember.room_id == room_id,
                RoomMember.role == "admin"
            ).count()
            
            if admin_count == 1:
                # Transfer admin to another member or delete room
                other_members = db.query(RoomMember).filter(
                    RoomMember.room_id == room_id,
                    RoomMember.user_id != user_id
                ).first()
                
                if other_members:
                    other_members.role = "admin"
                    db.commit()
                else:
                    # No other members, delete the room
                    room = db.query(Room).filter(Room.id == room_id).first()
                    room.is_active = False
                    db.commit()
        
        db.delete(membership)
        db.commit()
        
        return {"message": "Successfully left the room"}
