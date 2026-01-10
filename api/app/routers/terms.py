from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.term import Term
from app.models.program import Program
from app.models.enums import UserRole
from app.schemas.term import TermCreate, TermOut
from app.auth.dependencies import require_role
from app.routers.deps import get_db

router = APIRouter(
    prefix="/cms/programs/{program_id}/terms",
    tags=["cms-terms"]
)

# ✅ CREATE TERM
@router.post(
    "",
    response_model=TermOut,
    dependencies=[Depends(require_role(UserRole.admin, UserRole.editor))]
)
def create_term(
    program_id: str,
    data: TermCreate,
    db: Session = Depends(get_db)
):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    term = Term(
        program_id=program_id,
        term_number=data.term_number,
        title=data.title
    )

    db.add(term)
    db.commit()
    db.refresh(term)
    return term


# ✅ LIST TERMS FOR A PROGRAM
@router.get(
    "",
    response_model=List[TermOut],
    dependencies=[Depends(require_role(UserRole.admin, UserRole.editor, UserRole.viewer))]
)
def list_terms(
    program_id: str,
    db: Session = Depends(get_db)
):
    return (
        db.query(Term)
        .filter(Term.program_id == program_id)
        .order_by(Term.term_number)
        .all()
    )


# ✅ GET SINGLE TERM
@router.get(
    "/{term_id}",
    response_model=TermOut,
    dependencies=[Depends(require_role(UserRole.admin, UserRole.editor, UserRole.viewer))]
)
def get_term(
    program_id: str,
    term_id: str,
    db: Session = Depends(get_db)
):
    term = db.get(Term, term_id)
    if not term or term.program_id != program_id:
        raise HTTPException(status_code=404, detail="Term not found")
    return term
