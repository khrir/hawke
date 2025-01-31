from app.models.entities.event import Event
from infra.configs.base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime

class Activity(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    date = Column(String(10), nullable=False)
    start_time = Column(String(5), nullable=False)
    end_time = Column(String(5), nullable=False)
    status = Column(Integer, nullable=False, default=1)
    price = Column(Float, nullable=True)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    speaker_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
     
    event = relationship('Event', back_populates='activities')
    speaker = relationship('User')
 
    def __repr__(self):
        return f"<Activity(name={self.name}, date={self.date})>"
    
    def serialize(self) -> dict[str, any]:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'date': self.start_date,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'status': self.status,
            'price': self.price,
            'event_id': self.event_id,
            'speaker_id': self.speaker_id,
        }