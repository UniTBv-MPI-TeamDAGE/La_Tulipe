import type { RegisterRequest, LoginRequest, LoginResponse } from "../dtos/auth";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export async function registerUser(data: RegisterRequest): Promise<{ message: string }> {
  const res = await fetch(`${API_URL}/api/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  const json = await res.json();
  if (!res.ok) {
    throw { status: res.status, detail: json.detail ?? "Eroare necunoscută" };
  }
  return json;
}

export async function loginUser(data: LoginRequest): Promise<LoginResponse> {
  const res = await fetch(`${API_URL}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  const json = await res.json();
  if (!res.ok) {
    throw { status: res.status, detail: json.detail ?? "Eroare necunoscută" };
  }
  return json as LoginResponse;
}