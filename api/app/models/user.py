import uuid
from datetime import datetime
from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import Base
from app.models.enums import UserRole


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    email = Column(String, nullable=False, unique=True, index=True)
    password_hash = Column(String, nullable=False)

    role = Column(Enum(UserRole), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
