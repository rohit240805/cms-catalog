import { useEffect, useState, useCallback } from "react";
import { apiGet, apiPost } from "../api/api";
import "./Program.css";

export default function Programs({ token, onSelectProgram }) {
  const [programs, setPrograms] = useState([]);
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(false);

  // 🔄 Load programs (stable reference)
  const loadPrograms = useCallback(async () => {
    if (!token) return;

    setLoading(true);
    try {
      const data = await apiGet("/cms/programs", token);
      setPrograms(data);
    } finally {
      setLoading(false);
    }
  }, [token]);

  // 🔁 Fetch on login / token change
  useEffect(() => {
    loadPrograms();
  }, [loadPrograms]);

  // ➕ Create program AND redirect to Terms
  async function createProgram() {
    if (!title.trim()) {
      alert("Enter program title");
      return;
    }

    try {
      const program = await apiPost(
        "/cms/programs",
        {
          title,
          language_primary: "en",
          languages_available: ["en"],
        },
        token
      );

      setTitle("");
      onSelectProgram(program); // ✅ redirect immediately

    } catch (err) {
      console.error("Create program error:", err);
      alert(
        err?.message ||
        "Failed to create program (check console + API logs)"
      );
    }
  }

  return (
    <div className="page">
      <h2>Programs</h2>

      {/* ➕ Create Program */}
      <div className="create-bar">
        <input
          placeholder="New program title"
          value={title}
          onChange={e => setTitle(e.target.value)}
        />
        <button onClick={createProgram}>
          Create Program
        </button>
      </div>

      {/* 📋 Programs List */}
      {loading ? (
        <p>Loading programs...</p>
      ) : (
        <div className="grid">
          {programs.map(p => (
            <div className="card program-card" key={p.id}>
              <span className={`badge ${p.status}`}>
                {p.status}
              </span>

              <h3>{p.title}</h3>
              <p>{p.description || "No description"}</p>

              <button onClick={() => onSelectProgram(p)}>
                Manage →
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
