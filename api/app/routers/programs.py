from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.program import Program
from app.models.enums import UserRole
from app.auth.dependencies import require_role
from app.routers.deps import get_db
from app.schemas.program import ProgramCreate, ProgramOut
from app.models.program_asset import ProgramAsset
from app.models.enums import ProgramStatus
from app.schemas.program import ProgramUpdate


router = APIRouter(prefix="/cms/programs", tags=["cms-programs"])


@router.post(
    "",
    response_model=ProgramOut,
    dependencies=[Depends(require_role(UserRole.admin, UserRole.editor))]
)
def create_program(data: ProgramCreate, db: Session = Depends(get_db)):
    program = Program(**data.dict())
    db.add(program)
    db.commit()
    db.refresh(program)
    return program


@router.get(
    "",
    response_model=List[ProgramOut],
    dependencies=[Depends(require_role(UserRole.admin, UserRole.editor, UserRole.viewer))]
)
def list_programs(db: Session = Depends(get_db)):
    return db.query(Program).all()


@router.get(
    "/{program_id}",
    response_model=ProgramOut,
    dependencies=[Depends(require_role(UserRole.admin, UserRole.editor, UserRole.viewer))]
)
def get_program(program_id: str, db: Session = Depends(get_db)):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    return program


@router.put(
    "/{program_id}",
    response_model=ProgramOut,
    dependencies=[Depends(require_role(UserRole.admin, UserRole.editor))]
)
def update_program(
    program_id: str,
    data: ProgramUpdate,
    db: Session = Depends(get_db)
):
    program = db.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    # =====================================================
    # ✅ PROGRAM PUBLISH VALIDATION (CMS-GRADE)
    # =====================================================
    if data.status == ProgramStatus.published:

        assets = (
            db.query(ProgramAsset)
            .filter(
                ProgramAsset.program_id == program.id,
                ProgramAsset.language == program.language_primary,
                ProgramAsset.asset_type == "poster"
            )
            .all()
        )

        variants = {a.variant for a in assets}
        required = {"portrait", "landscape"}

        if not required.issubset(variants):
            raise HTTPException(
                status_code=400,
                detail=(
                    "Primary language must have "
                    "portrait and landscape poster assets before publishing"
                )
            )

        program.published_at = datetime.utcnow()

    # Apply updates
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(program, k, v)

    db.commit()
    db.refresh(program)
    return program
