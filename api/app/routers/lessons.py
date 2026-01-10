from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.lesson import Lesson
from app.models.term import Term
from app.models.enums import UserRole, LessonStatus
from app.schemas.lesson import LessonCreate, LessonOut, LessonUpdate
from app.auth.dependencies import require_role
from app.routers.deps import get_db

router = APIRouter(
    prefix="/cms/terms/{term_id}/lessons",
    tags=["cms-lessons"]
)

# =========================================================
# CREATE lesson (draft OR scheduled)
# =========================================================
@router.post(
    "",
    response_model=LessonOut,
    dependencies=[Depends(require_role(UserRole.admin, UserRole.editor))]
)
def create_lesson(
    term_id: str,
    data: LessonCreate,
    db: Session = Depends(get_db)
):
    term = db.get(Term, term_id)
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")

    # ✅ enforce schedule rules
    if data.status == LessonStatus.scheduled and not data.publish_at:
        raise HTTPException(
            status_code=400,
            detail="publish_at required when status=scheduled"
        )

    lesson = Lesson(
        term_id=term_id,
        **data.model_dump()
    )

    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson



# =========================================================
# LIST lessons
# =========================================================
@router.get(
    "",
    response_model=List[LessonOut],
    dependencies=[Depends(require_role(
        UserRole.admin, UserRole.editor, UserRole.viewer
    ))]
)
def list_lessons(term_id: str, db: Session = Depends(get_db)):
    return (
        db.query(Lesson)
        .filter(Lesson.term_id == term_id)
        .order_by(Lesson.lesson_number)
        .all()
    )


# =========================================================
# GET single lesson
# =========================================================
@router.get(
    "/{lesson_id}",
    response_model=LessonOut,
    dependencies=[Depends(require_role(
        UserRole.admin, UserRole.editor, UserRole.viewer
    ))]
)
def get_lesson(term_id: str, lesson_id: str, db: Session = Depends(get_db)):
    lesson = db.get(Lesson, lesson_id)
    if not lesson or lesson.term_id != term_id:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


# =========================================================
# UPDATE lesson (not published)
# =========================================================
@router.put(
    "/{lesson_id}",
    response_model=LessonOut,
    dependencies=[Depends(require_role(UserRole.admin, UserRole.editor))]
)
def update_lesson(
    term_id: str,
    lesson_id: str,
    data: LessonUpdate,
    db: Session = Depends(get_db)
):
    lesson = db.get(Lesson, lesson_id)
    if not lesson or lesson.term_id != term_id:
        raise HTTPException(status_code=404, detail="Lesson not found")

    if lesson.status == LessonStatus.published:
        raise HTTPException(
            status_code=400,
            detail="Cannot edit published lesson"
        )

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(lesson, k, v)

    db.commit()
    db.refresh(lesson)
    return lesson


# =========================================================
# ARCHIVE lesson
# =========================================================
@router.post(
    "/{lesson_id}/archive",
    dependencies=[Depends(require_role(UserRole.admin, UserRole.editor))]
)
def archive_lesson(
    term_id: str,
    lesson_id: str,
    db: Session = Depends(get_db)
):
    lesson = db.get(Lesson, lesson_id)
    if not lesson or lesson.term_id != term_id:
        raise HTTPException(status_code=404, detail="Lesson not found")

    if lesson.status == LessonStatus.archived:
        return {"id": lesson.id, "status": "already archived"}

    lesson.status = LessonStatus.archived
    db.commit()
    db.refresh(lesson)

    return {"id": lesson.id, "status": lesson.status}
