from infra.configs.base import Base
from app.models.entities.user import User
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    start_date = Column(String(10), nullable=False)
    end_date = Column(String(10), nullable=False)
    slug = Column(String(50), nullable=False)
    status = Column(Integer, nullable=False, default=1)
    organizer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    user = relationship('User')
    address = relationship('EventAddress', uselist=False, back_populates='event', lazy='subquery')
    activities = relationship('Activity', back_populates='event', lazy='subquery')

    def __repr__(self):
        return f"<Event(name={self.name}, date={self.date})>"
    
    def serialize(self) -> dict[str, any]:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'slug': self.slug,
            'status': self.status,
            'user_id': self.organizer_id
        }

    def serialize_full(self) -> dict[str, any]:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'slug': self.slug,
            'status': self.status,
            'user_id': self.organizer_id,
            'address': self.address.serialize()
        }