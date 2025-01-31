from infra.configs.base import Base
from app.models.entities.event import Event
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Time
from sqlalchemy.orm import relationship
from datetime import datetime

class TicketLot(Base):
    __tablename__ = 'ticket_lots'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Integer, nullable=True)
    quantity = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    start_date = Column(Time, nullable=True)
    end_date = Column(Time, nullable=True)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    event = relationship('Event')

    def __repr__(self):
        return f"<TicketLot(name={self.name}, price={self.price}, quantity={self.quantity})>"


