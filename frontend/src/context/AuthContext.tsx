import { createContext, useContext, useState, useEffect, type ReactNode } from "react";

interface User {
  token: string;
  name: string;
  role: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  login: (data: { access_token: string; name: string; role: string; email: string }) => void;
  logout: () => void;
  updateUser: (data: { name?: string; phone?: string }) => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = sessionStorage.getItem("access_token");
    const name = sessionStorage.getItem("user_name");
    const role = sessionStorage.getItem("user_role");
    const email = sessionStorage.getItem("user_email");
    if (token && name && role && email) {
      setUser({ token, name, role, email });
    }
    setLoading(false);
  }, []);

  const login = (data: { access_token: string; name: string; role: string ; email:string}) => {
    sessionStorage.setItem("access_token", data.access_token);
    sessionStorage.setItem("user_name", data.name);
    sessionStorage.setItem("user_role", data.role);
    sessionStorage.setItem("user_email", data.email);
    setUser({ token: data.access_token, name: data.name, role: data.role , email: data.email});
  };

  const logout = () => {
    sessionStorage.removeItem("access_token");
    sessionStorage.removeItem("user_name");
    sessionStorage.removeItem("user_role");
    sessionStorage.removeItem("user_email"); 
    setUser(null);
  };

  const updateUser = (data: { name?: string; phone?: string }) => {
    if (!user) return;
    if (data.name) {
      sessionStorage.setItem("user_name", data.name);
      setUser((prev) => prev ? { ...prev, name: data.name! } : prev);
    }
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, updateUser, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextType {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
  return ctx;
}