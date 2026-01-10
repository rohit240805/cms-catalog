import { useState } from "react";
import Login from "./pages/Login";
import Programs from "./pages/Programs";
import Terms from "./pages/Terms";
import Lessons from "./pages/Lessons";
import Catalog from "./pages/Catalog";

export default function App() {
  const [auth, setAuth] = useState(null);
  const [program, setProgram] = useState(null);
  const [term, setTerm] = useState(null);

  // 🔓 NOT LOGGED IN → PUBLIC CATALOG
  if (!auth) {
    return <Login onLogin={setAuth} />;
  }

  // 👀 VIEWER → CATALOG ONLY
  if (auth.role === "viewer") {
    return <Catalog />;
  }

  // 🔐 ADMIN / EDITOR → CMS
  if (!program) {
    return (
      <Programs
        token={auth.token}
        onSelectProgram={setProgram}
      />
    );
  }

  if (!term) {
    return (
      <Terms
        token={auth.token}
        program={program}
        onSelectTerm={setTerm}
      />
    );
  }

  return (
    <Lessons
      token={auth.token}
      term={term}
    />
  );
}
