import { useEffect, useState, useCallback } from "react";
import { apiGet, apiPost } from "../api/api";
import "./Lessons.css";

export default function Lessons({ token, term }) {
  const [lessons, setLessons] = useState([]);
  const [lessonNumber, setLessonNumber] = useState(1);
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(false);

  // 🔄 Stable loader (ESLint + React safe)
  const loadLessons = useCallback(async () => {
    if (!term?.id) return;

    setLoading(true);
    try {
      const data = await apiGet(
        `/cms/terms/${term.id}/lessons`,
        token
      );
      setLessons(data);
    } finally {
      setLoading(false);
    }
  }, [term?.id, token]);

  // 🔁 Load when term changes
  useEffect(() => {
    loadLessons();
  }, [loadLessons]);

  // 📝 Create Draft
  async function createDraft() {
    if (!title.trim()) {
      alert("Enter lesson title");
      return;
    }

    try {
      await apiPost(
        `/cms/terms/${term.id}/lessons`,
        {
          lesson_number: lessonNumber,
          title,
          content_type: "video",
          content_language_primary: "en",
          content_languages_available: ["en"],
          content_urls_by_language: {
            en: "https://example.com/video"
          },
          status: "draft"
        },
        token
      );

      setLessonNumber(n => n + 1);
      setTitle("");
      loadLessons(); // ✅ safe reuse
    } catch (err) {
      console.error(err);
      alert("Failed to create draft lesson");
    }
  }

  // ⏱ Schedule Lesson
  async function scheduleLesson() {
    if (!title.trim()) {
      alert("Enter lesson title");
      return;
    }

    const publishAt = new Date(
      Date.now() + 2 * 60 * 1000
    ).toISOString();

    try {
      await apiPost(
        `/cms/terms/${term.id}/lessons`,
        {
          lesson_number: lessonNumber,
          title,
          content_type: "video",
          content_language_primary: "en",
          content_languages_available: ["en"],
          content_urls_by_language: {
            en: "https://example.com/video"
          },
          status: "scheduled",
          publish_at: publishAt
        },
        token
      );

      setLessonNumber(n => n + 1);
      setTitle("");
      loadLessons(); // ✅ safe reuse
    } catch (err) {
      console.error(err);
      alert("Failed to schedule lesson");
    }
  }

  return (
    <div className="page">
      <h2>Lessons → Term {term.term_number}</h2>

      {/* ➕ Lesson Editor */}
      <div className="lesson-editor">
        <input
          placeholder="Lesson title"
          value={title}
          onChange={e => setTitle(e.target.value)}
        />

        <div className="actions">
          <button onClick={createDraft}>
            Save Draft
          </button>

          <button onClick={scheduleLesson}>
            Schedule (+2 min)
          </button>
        </div>
      </div>

      {/* 📋 Lessons List */}
      {loading ? (
        <p>Loading lessons...</p>
      ) : (
        <div className="grid">
          {lessons.map(l => (
            <div className="card" key={l.id}>
              <span className={`badge ${l.status}`}>
                {l.status}
              </span>

              <h3>
                {l.lesson_number}. {l.title}
              </h3>

              {l.publish_at && (
                <p>
                  ⏰ Publish at:{" "}
                  {new Date(l.publish_at).toLocaleString()}
                </p>
              )}

              {l.published_at && (
                <p>
                  ✅ Published:{" "}
                  {new Date(l.published_at).toLocaleString()}
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
