import { useState } from "react";
import { apiPost } from "../api/api";
import { parseJwt } from "../api/auth";
import "./Login.css";

export default function Login({ onLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function handleLogin(e) {
    e.preventDefault();

    try {
      const res = await apiPost(
        "/auth/login",
        { email, password },
        null // ⬅️ NO token for login
      );

      const token = res.access_token;
      const payload = parseJwt(token);

      // ✅ SINGLE SOURCE OF TRUTH
      onLogin({
        token,
        role: payload.role
      });

    } catch (err) {
      console.error(err);
      alert("Invalid credentials");
    }
  }

  return (
    <div className="login-page">
      <form className="login-card" onSubmit={handleLogin}>
        <h2>CMS Login</h2>

        <input
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
        />

        <button type="submit">Login</button>
      </form>
    </div>
  );
}
