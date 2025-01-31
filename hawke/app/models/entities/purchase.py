from infra.configs.base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

class Purchase(Base):
    __tablename__ = 'purchases'

    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    ticket_lot_id = Column(Integer, ForeignKey('ticket_lots.id'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    user = relationship('User')
    ticket_lot = relationship('TicketLot')

    def __repr__(self):
        return f"<Purchase(quantity={self.quantity}, total={self.total})>"

    def serialize(self) -> dict[str, any]:
        return {
            'id': self.id,
            'quantity': self.quantity,
            'total': self.total,
            'user_id': self.user_id,
            'ticket_lot_id': self.ticket_lot_id
        }