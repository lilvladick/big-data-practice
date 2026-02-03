from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, TIMESTAMP, UUID
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(UUID, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    patronymic = Column(String(50), nullable=True)
    email = Column(String(50), unique=True, index=True)
    password_hash = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.now(timezone.utc))

    user_roles = relationship("UserRole", back_populates="user")
    roles = association_proxy("user_roles", "role")
