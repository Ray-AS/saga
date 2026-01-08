const BACKEND_URL = process.env.BACKEND_URL ?? "http://localhost:8000";

export async function fetchFromAPI<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const res = await fetch(`${BACKEND_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    cache: "no-store",
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Backend error ${res.status}: ${text}`);
  }

  if (res.status === 204) return null as T;

  return res.json() as Promise<T>;
}
