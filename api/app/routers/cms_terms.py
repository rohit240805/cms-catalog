from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.term import Term
from app.models.enums import UserRole
from app.auth.dependencies import require_role
from app.routers.deps import get_db

router = APIRouter(prefix="/cms/terms", tags=["cms-terms"])

@router.post("", dependencies=[Depends(require_role(UserRole.admin, UserRole.editor))])
def create_term(data: dict, db: Session = Depends(get_db)):
    term = Term(**data)
    db.add(term)
    db.commit()
    return term
