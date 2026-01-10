import uuid
from datetime import datetime
from sqlalchemy import Column, Text, String, Enum, DateTime, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base
from app.models.enums import ProgramStatus


class Program(Base):
    __tablename__ = "programs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    title = Column(Text, nullable=False)
    description = Column(Text)

    language_primary = Column(String, nullable=False)
    languages_available = Column(ARRAY(String), nullable=False)

    status = Column(
        Enum(ProgramStatus),
        nullable=False,
        default=ProgramStatus.draft
    )

    published_at = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
