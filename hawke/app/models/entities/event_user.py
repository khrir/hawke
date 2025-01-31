from infra.configs.base import Base
from app.models.entities.event import Event
from app.models.entities.user import User
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class EventUser(Base):
    __tablename__ = 'event_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    event = relationship('Event')
    user = relationship('User')

    def __repr__(self):
        return f"<EventUser(event_id={self.event_id}, user_id={self.user_id})>"
    
    def serialize(self) -> dict[str, any]:
        return {
            "id": self.id,
            "event_id": self.event_id,
            "user_id": self.user_id
        }