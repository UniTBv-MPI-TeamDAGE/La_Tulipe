import type { RegisterRequest, LoginRequest, LoginResponse, UserMeResponse, UpdateMeRequest } from "../dtos/auth";

const API_URL = "";

export async function registerUser(data: RegisterRequest): Promise<{ message: string }> {
  const payload = {
    ...data,
    phone: data.phone?.trim() || null,
    admin_code: data.admin_code?.trim() || null,
  };

  console.log("Sending payload:", JSON.stringify(payload, null, 2));  

  const res = await fetch(`${API_URL}/api/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const json = await res.json();
  console.log("Response:", JSON.stringify(json, null, 2));  
  if (!res.ok) throw { status: res.status, detail: json.detail ?? "Unknown error" };
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

export async function getUserMe(token?: string): Promise<UserMeResponse> {
  const t = token ?? sessionStorage.getItem("access_token");
  const res = await fetch(`${API_URL}/api/users/me`, {
    headers: { Authorization: `Bearer ${t}` },
  });
  const json = await res.json();
  if (!res.ok) throw { status: res.status, detail: json.detail ?? "Unknown error" };
  return json as UserMeResponse;
}

export async function updateUserMe(data: UpdateMeRequest): Promise<UserMeResponse> {
  const token = sessionStorage.getItem("access_token");
  const res = await fetch(`${API_URL}/api/users/me`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(data),
  });
  const json = await res.json();
  if (!res.ok) throw { status: res.status, detail: json.detail ?? "Eroare necunoscută" };
  return json as UserMeResponse;
}