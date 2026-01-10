import uuid
from sqlalchemy import Column, Text, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base
from app.models.enums import AssetVariant


class LessonAsset(Base):
    __tablename__ = "lesson_assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    lesson_id = Column(
        UUID(as_uuid=True),
        ForeignKey("lessons.id"),
        nullable=False
    )

    language = Column(Text, nullable=False)
    variant = Column(Enum(AssetVariant), nullable=False)
    asset_type = Column(Text, nullable=False, default="thumbnail")

    url = Column(Text, nullable=False)
