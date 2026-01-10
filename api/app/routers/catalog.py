from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.program import Program
from app.models.term import Term
from app.models.lesson import Lesson
from app.models.program_asset import ProgramAsset
from app.models.lesson_asset import LessonAsset

router = APIRouter(prefix="/catalog", tags=["catalog"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.get("/programs")
def list_programs(db: Session = Depends(get_db)):
    programs = (
        db.query(Program)
        .filter(Program.status == "published")
        .order_by(Program.published_at.desc())
        .all()
    )

    response = []
    for p in programs:
        assets = (
            db.query(ProgramAsset)
            .filter(ProgramAsset.program_id == p.id)
            .all()
        )

        posters = {}
        for a in assets:
            posters.setdefault(a.variant, {})[a.language] = a.url

        response.append({
            "id": str(p.id),
            "title": p.title,
            "description": p.description,
            "language": p.language_primary,
            "posters": posters
        })

    return response
@router.get("/programs/{program_id}")
def program_detail(program_id: str, db: Session = Depends(get_db)):
    program = (
        db.query(Program)
        .filter(
            Program.id == program_id,
            Program.status == "published"
        )
        .first()
    )

    if not program:
        return {"detail": "Not found"}

    terms = (
        db.query(Term)
        .filter(Term.program_id == program.id)
        .order_by(Term.term_number)
        .all()
    )

    term_data = []
    for t in terms:
        lessons = (
            db.query(Lesson)
            .filter(
                Lesson.term_id == t.id,
                Lesson.status == "published"
            )
            .order_by(Lesson.lesson_number)
            .all()
        )

        lesson_data = []
        for l in lessons:
            lesson_data.append({
                "lesson_number": l.lesson_number,
                "title": l.title,
                "is_paid": l.is_paid,
                "duration_ms": l.duration_ms,
                "content_url": l.content_urls_by_language.get(
                    l.content_language_primary
                )
            })

        term_data.append({
            "term_number": t.term_number,
            "title": t.title,
            "lessons": lesson_data
        })

    return {
        "id": str(program.id),
        "title": program.title,
        "description": program.description,
        "terms": term_data
    }
