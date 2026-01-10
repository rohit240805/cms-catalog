import uuid
from sqlalchemy import Column, Text, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base
from app.models.enums import AssetVariant


class ProgramAsset(Base):
    __tablename__ = "program_assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    program_id = Column(
        UUID(as_uuid=True),
        ForeignKey("programs.id"),
        nullable=False
    )

    language = Column(Text, nullable=False)
    variant = Column(Enum(AssetVariant), nullable=False)
    asset_type = Column(Text, nullable=False, default="poster")

    url = Column(Text, nullable=False)
