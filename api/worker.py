import time
from datetime import datetime, timezone

from sqlalchemy.orm import Session  # type: ignore


from app.database import SessionLocal
from app.models.lesson import Lesson
from app.models.enums import LessonStatus


def publish_lesson(db: Session, lesson: Lesson):
    """
    Publish a scheduled lesson
    """
    lesson.status = LessonStatus.published
    lesson.published_at = datetime.now(timezone.utc)
    lesson.publish_at = None  # prevent re-processing

    print(f"✅ Published lesson {lesson.id}")


def run():
    print("🚀 Worker started — watching for scheduled lessons")

    while True:
        db = SessionLocal()
        try:
            now = datetime.now(timezone.utc)

            lessons = (
                db.query(Lesson)
                .filter(
                    Lesson.status == LessonStatus.scheduled,
                    Lesson.publish_at <= now
                )
                .all()
            )

            if lessons:
                print(f"⏳ Found {len(lessons)} lesson(s) to publish")

            for lesson in lessons:
                publish_lesson(db, lesson)

            db.commit()

        except Exception as e:
            db.rollback()
            print("❌ Worker error:", e)

        finally:
            db.close()

        time.sleep(30)  # poll every 30 seconds


if __name__ == "__main__":
    run()
