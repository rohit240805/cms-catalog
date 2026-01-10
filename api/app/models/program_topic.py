from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class ProgramTopic(Base):
    __tablename__ = "program_topics"

    program_id = Column(
        UUID(as_uuid=True),
        ForeignKey("programs.id"),
        primary_key=True
    )

    topic_id = Column(
        UUID(as_uuid=True),
        ForeignKey("topics.id"),
        primary_key=True
    )
