export interface RegisterRequest {
  name: string;
  email: string;
  password: string;
  confirm_password: string;
  phone?: string;
  role: "customer" | "admin";
  admin_code?: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  name: string;
  role: string;
}

export interface UserMeResponse{
  name: string;
  email: string;
  phone?: string;
}

export interface UpdateMeRequest{
  name?: string;
  phone?: string;
}
