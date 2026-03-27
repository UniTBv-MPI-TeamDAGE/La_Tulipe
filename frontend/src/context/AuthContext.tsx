import { createContext, useContext, useState, useEffect, type ReactNode } from "react";

interface User {
  token: string;
  nume: string;
  role: string;
}

interface AuthContextType {
  user: User | null;
  login: (data: { access_token: string; nume: string; role: string }) => void;
  logout: () => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    const nume = localStorage.getItem("user_nume");
    const role = localStorage.getItem("user_role");
    if (token && nume && role) {
      setUser({ token, nume, role });
    }
    setLoading(false);
  }, []);

  const login = (data: { access_token: string; nume: string; role: string }) => {
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("user_nume", data.nume);
    localStorage.setItem("user_role", data.role);
    setUser({ token: data.access_token, nume: data.nume, role: data.role });
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_nume");
    localStorage.removeItem("user_role");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextType {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
  return ctx;
}