from datetime import datetime, timedelta
from sqlalchemy import text
from app.database import SessionLocal
from app.models.program import Program
from app.models.term import Term
from app.models.lesson import Lesson
from app.models.enums import ProgramStatus, LessonStatus, UserRole
from app.auth.password import hash_password






def run():
    db = SessionLocal()

    # ---------- USERS (RAW SQL, SAFE) ----------
    db.execute(text("""
        INSERT INTO users (id, email, password_hash, role, created_at)
        VALUES
          (gen_random_uuid(), 'admin@cms.com', :admin_pw, 'admin', now()),
          (gen_random_uuid(), 'editor@cms.com', :editor_pw, 'editor', now()),
          (gen_random_uuid(), 'viewer@cms.com', :viewer_pw, 'viewer', now())
        ON CONFLICT (email) DO NOTHING
    """), {
        "admin_pw": hash_password("admin123"),
        "editor_pw": hash_password("editor123"),
        "viewer_pw": hash_password("viewer123"),
    })

    db.commit()


    # ---------- PROGRAM ----------
    program = db.query(Program).filter_by(title="Demo Program").first()
    if not program:
        program = Program(
            title="Demo Program",
            description="End-to-end CMS demo program",
            language_primary="en",
            languages_available=["en"],
            status=ProgramStatus.published,
            published_at=datetime.utcnow()
        )
        db.add(program)
        db.commit()
        db.refresh(program)

    # ---------- TERM ----------
    term = (
        db.query(Term)
        .filter_by(program_id=program.id, term_number=1)
        .first()
    )
    if not term:
        term = Term(
            program_id=program.id,
            term_number=1,
            title="Introduction"
        )
        db.add(term)
        db.commit()
        db.refresh(term)

    # ---------- PUBLISHED LESSON ----------
    lesson1 = (
        db.query(Lesson)
        .filter_by(term_id=term.id, lesson_number=1)
        .first()
    )
    if not lesson1:
        lesson1 = Lesson(
            term_id=term.id,
            lesson_number=1,
            title="Welcome Lesson",
            content_type="video",
            content_language_primary="en",
            content_languages_available=["en"],
            content_urls_by_language={"en": "https://example.com/welcome"},
            status=LessonStatus.published,
            published_at=datetime.utcnow()
        )
        db.add(lesson1)

    # ---------- SCHEDULED LESSON (WORKER TEST) ----------
    lesson2 = (
        db.query(Lesson)
        .filter_by(term_id=term.id, lesson_number=2)
        .first()
    )
    if not lesson2:
        lesson2 = Lesson(
            term_id=term.id,
            lesson_number=2,
            title="Scheduled Lesson",
            content_type="video",
            content_language_primary="en",
            content_languages_available=["en"],
            content_urls_by_language={"en": "https://example.com/scheduled"},
            status=LessonStatus.scheduled,
            publish_at=datetime.utcnow() + timedelta(minutes=2)
        )
        db.add(lesson2)

    db.commit()
    db.close()

    print("✅ Seed completed (idempotent)")


if __name__ == "__main__":
    run()
