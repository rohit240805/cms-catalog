import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class Term(Base):
    __tablename__ = "terms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    program_id = Column(
        UUID(as_uuid=True),
        ForeignKey("programs.id"),
        nullable=False
    )

    term_number = Column(Integer, nullable=False)
    title = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)
