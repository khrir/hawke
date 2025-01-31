from infra.configs.base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Float, nullable=False)
    status = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    purchase_id = Column(Integer, ForeignKey('purchases.id'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    user = relationship('User')
    purchase = relationship('Purchase')

    def __repr__(self):
        return f"<Payment(amount={self.amount}, status={self.status})>"

    def serialize(self) -> dict[str, any]:
        return {
            'id': self.id,
            'amount': self.amount,
            'status': self.status,
            'user_id': self.user_id,
            'purchase_id': self.purchase_id
        }