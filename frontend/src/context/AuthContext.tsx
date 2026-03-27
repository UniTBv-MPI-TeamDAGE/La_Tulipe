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
    const token = localStorage.getItem("access_token");
    const name = localStorage.getItem("user_name");
    const role = localStorage.getItem("user_role");
    const email = localStorage.getItem("user_email");
    if (token && name && role && email) {
      setUser({ token, name, role, email });
    }
    setLoading(false);
  }, []);

  const login = (data: { access_token: string; name: string; role: string ; email:string}) => {
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("user_name", data.name);
    localStorage.setItem("user_role", data.role);
    localStorage.setItem("user_email", data.email);
    setUser({ token: data.access_token, name: data.name, role: data.role , email: data.email});
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_name");
    localStorage.removeItem("user_role");
    localStorage.removeItem("user_email"); 
    setUser(null);
  };

  const updateUser = (data: { name?: string; phone?: string }) => {
    if (!user) return;
    if (data.name) {
      localStorage.setItem("user_name", data.name);
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