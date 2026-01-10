from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class TermCreate(BaseModel):
    term_number: int
    title: str

class TermOut(BaseModel):
    id: UUID
    program_id: UUID
    term_number: int
    title: str | None
    created_at: datetime

    class Config:
        from_attributes = True
