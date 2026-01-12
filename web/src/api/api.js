const BASE_URL = "https://cms-catalog-api.onrender.com";

export async function apiGet(path, token) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: token
      ? { Authorization: `Bearer ${token}` }
      : {}
  });

  if (!res.ok) {
    throw new Error(await res.text());
  }

  return res.json();
}

export async function apiPost(path, body, token) {
  const headers = {
    "Content-Type": "application/json"
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const res = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers,
    body: JSON.stringify(body)
  });

  if (!res.ok) {
    throw new Error(await res.text());
  }

  return res.json();
}
