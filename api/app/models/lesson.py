import uuid
from datetime import datetime
from sqlalchemy import (
    Column, Integer, Text, Enum, DateTime,
    Boolean, ForeignKey, ARRAY
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.models.base import Base
from app.models.enums import LessonStatus


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    term_id = Column(
        UUID(as_uuid=True),
        ForeignKey("terms.id"),
        nullable=False
    )

    lesson_number = Column(Integer, nullable=False)
    title = Column(Text, nullable=False)

    content_type = Column(
        Enum("video", "article", name="content_type"),
        nullable=False
    )

    duration_ms = Column(Integer)
    is_paid = Column(Boolean, default=False)

    content_language_primary = Column(Text, nullable=False)
    content_languages_available = Column(ARRAY(Text), nullable=False)
    content_urls_by_language = Column(JSONB, nullable=False)

    subtitle_languages = Column(ARRAY(Text))
    subtitle_urls_by_language = Column(JSONB)

    status = Column(
        Enum(LessonStatus),
        nullable=False,
        default=LessonStatus.draft
    )

    publish_at = Column(DateTime)
    published_at = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
