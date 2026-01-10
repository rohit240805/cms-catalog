import { useEffect, useState, useCallback } from "react";
import { apiGet, apiPost } from "../api/api";
import "./Terms.css";

export default function Terms({ token, program, onSelectTerm }) {
  const [terms, setTerms] = useState([]);
  const [termNumber, setTermNumber] = useState(1);
  const [loading, setLoading] = useState(false);

  // ✅ STABLE function
  const loadTerms = useCallback(async () => {
    if (!program?.id) return;

    setLoading(true);
    try {
      const data = await apiGet(
        `/cms/programs/${program.id}/terms`,
        token
      );
      setTerms(data);
    } finally {
      setLoading(false);
    }
  }, [program?.id, token]);

  async function createTerm() {
    try {
      await apiPost(
        `/cms/programs/${program.id}/terms`,
        {
          term_number: termNumber,
          title: `Term ${termNumber}`,
        },
        token
      );

      setTermNumber(n => n + 1);
      loadTerms(); // ✅ safe reuse
    } catch (err) {
      console.error(err);
      alert("Failed to create term");
    }
  }

  // ✅ ESLint-safe, React-safe
  useEffect(() => {
    loadTerms();
  }, [loadTerms]);

  return (
    <div className="page">
      <h2>{program.title} → Terms</h2>

      <div className="create-bar">
        <button onClick={createTerm}>+ Add Term</button>
      </div>

      {loading ? (
        <p>Loading terms...</p>
      ) : (
        <div className="grid">
          {terms.map(t => (
            <div className="card" key={t.id}>
              <h3>Term {t.term_number}</h3>
              <p>{t.title || "No title"}</p>

              <button onClick={() => onSelectTerm(t)}>
                Manage Lessons →
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
