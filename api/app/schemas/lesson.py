from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
from uuid import UUID
from app.models.enums import LessonStatus


class LessonCreate(BaseModel):
    lesson_number: int
    title: str
    content_type: str
    content_language_primary: str
    content_languages_available: List[str]
    content_urls_by_language: Dict[str, str]
    status: LessonStatus
    publish_at: Optional[datetime] = None


class LessonUpdate(BaseModel):
    title: Optional[str] = None
    content_urls_by_language: Optional[Dict[str, str]] = None
    publish_at: Optional[datetime] = None
    status: Optional[LessonStatus] = None


class LessonOut(BaseModel):
    id: UUID
    term_id: UUID
    lesson_number: int
    title: str
    content_type: str
    content_language_primary: str
    content_languages_available: List[str]
    content_urls_by_language: Dict[str, str]
    status: LessonStatus
    publish_at: Optional[datetime] = None
    published_at: Optional[datetime] = None

    class Config:
        from_attributes = True
