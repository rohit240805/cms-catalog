const BASE_URL = "https://cms-catalog-api.onrender.com";

/**
 * GET requests (protected or public)
 */
export async function apiGet(path, token) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: token
      ? {
          Authorization: `Bearer ${token}`,
        }
      : {},
  });

  if (!res.ok) {
    throw new Error(await res.text());
  }

  return res.json();
}

/**
 * POST requests with JSON body (ALL NON-AUTH APIs)
 */
export async function apiPost(path, body, token) {
  const headers = {
    "Content-Type": "application/json",
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const res = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers,
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    throw new Error(await res.text());
  }

  return res.json();
}

/**
 * LOGIN (OAuth2 Password Flow)
 * FastAPI REQUIRES:
 * - application/x-www-form-urlencoded
 * - fields: username, password
 */
export async function login(email, password) {
  const formData = new URLSearchParams();
  formData.append("username", email); // OAuth2 requires "username"
  formData.append("password", password);

  const res = await fetch(`${BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: formData,
  });

  if (!res.ok) {
    throw new Error(await res.text());
  }

  return res.json();
}
