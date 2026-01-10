import { useEffect, useState } from "react";
import { apiGet } from "../api/api";

export default function Catalog() {
  const [programs, setPrograms] = useState([]);

  useEffect(() => {
    apiGet("/catalog/programs")
      .then(setPrograms)
      .catch(console.error);
  }, []);

  return (
    <div>
      <h2>Public Catalog</h2>
      <ul>
        {programs.map(p => (
          <li key={p.id}>
            <strong>{p.title}</strong>
          </li>
        ))}
      </ul>
    </div>
  );
}
