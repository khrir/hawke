from infra.configs.base import Base
from app.models.entities.event import Event
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class EventAddress(Base):
    __tablename__ = 'event_addresses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    local = Column(String(50), nullable=False)
    neighborhood = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    zip_code = Column(String(10), nullable=False)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    event = relationship('Event', back_populates='address')

    def __repr__(self):
        return f"<Address(local={self.local}, number={self.number}, neighborhood={self.neighborhood})>"
    
    def serialize(self) -> dict[str, any]:
        return {
            "id": self.id,
            "local": self.local,
            "neighborhood": self.neighborhood,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code
        }