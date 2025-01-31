from infra.configs.base import Base
from app.models.entities.role import Role
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    email = Column(String(120), nullable=False)
    password = Column(String(255), nullable=False)
    role_id = Column(Integer, nullable=False, default=3)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"[User(id={self.id}, username={self.username})]"
    
    def serialize(self) -> dict[str, any]:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }
    
    def getId(self) -> int:
        return self.id