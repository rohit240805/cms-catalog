const BASE_URL = "https://cms-catalog-api.onrender.com";

/**
 * GET requests
 */
export async function apiGet(path, token) {
  const headers = {};

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const res = await fetch(`${BASE_URL}${path}`, { headers });

  if (!res.ok) {
    throw new Error(await res.text());
  }

  return res.json();
}

/**
 * POST requests
 * - Uses FORM DATA for /auth/login (OAuth2)
 * - Uses JSON for all other endpoints
 */
export async function apiPost(path, body, token) {
  let headers = {};
  let payload;

  // 🔑 OAuth2 login → MUST be form-urlencoded
  if (path === "/auth/login") {
    headers["Content-Type"] = "application/x-www-form-urlencoded";

    payload = new URLSearchParams({
      username: body.email,   // IMPORTANT
      password: body.password
    }).toString();
  } else {
    headers["Content-Type"] = "application/json";
    payload = JSON.stringify(body);

    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }
  }

  const res = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers,
    body: payload
  });

  if (!res.ok) {
    throw new Error(await res.text());
  }

  return res.json();
}
