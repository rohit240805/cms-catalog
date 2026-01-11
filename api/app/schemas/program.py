from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from typing import Optional, List
from app.models.enums import ProgramStatus

class ProgramUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    language_primary: Optional[str] = None
    languages_available: Optional[List[str]] = None
    status: Optional[ProgramStatus] = None



class ProgramCreate(BaseModel):
    title: str
    description: Optional[str] = None
    language_primary: str
    languages_available: List[str]

class ProgramUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    language_primary: Optional[str] = None
    languages_available: Optional[List[str]] = None
    status: Optional[ProgramStatus] = None


class ProgramOut(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    language_primary: str
    languages_available: List[str]
    status: str
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
