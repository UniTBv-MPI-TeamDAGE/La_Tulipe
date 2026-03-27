export interface RegisterRequest {
  nume: string;
  email: string;
  password: string;
  confirm_password: string;
  telefon?: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  nume: string;
  role: string;
}