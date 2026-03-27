import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import LoginPage from "./pages/login/LoginPage";
import RegisterPage from "./pages/register/RegisterPage";
import type { ReactNode } from "react";

function PrivateRoute({ children }: { children: ReactNode }) {
  const { user, loading } = useAuth();
  if (loading) return null;
  return user ? <>{children}</> : <Navigate to="/login" replace />;
}

function HomePage() {
  const { user, logout } = useAuth();
  return (
    <div style={{ padding: 40, fontFamily: "'Open Sans', sans-serif", color: "#444" }}>
      <h2 style={{ color: "#74867A", marginBottom: 8 }}>Bună, {user?.nume}! 🌷</h2>
      <p style={{ color: "#BDB4AC", marginBottom: 20 }}>Rol: {user?.role}</p>
      <button onClick={logout} style={{ padding: "10px 20px", background: "#74867A", color: "#fff", border: "none", borderRadius: 8, cursor: "pointer", fontSize: 13 }}>
        Ieși din cont
      </button>
    </div>
  );
}

function AdminRoute({ children }: { children: ReactNode }) {
  const { user, loading } = useAuth();
  if (loading) return null;
  if (!user) return <Navigate to="/login" replace />;
  if (user.role !== "admin") return <Navigate to="/" replace />;
  return <>{children}</>;
}

function AdminPage() {
  const { user, logout } = useAuth();
  return (
    <div style={{ padding: 40, fontFamily: "'Open Sans', sans-serif", color: "#444" }}>
      <h2 style={{ color: "#74867A", marginBottom: 8 }}>Dashboard Admin</h2>
      <p style={{ color: "#BDB4AC", marginBottom: 20 }}>Logat ca: {user?.nume}</p>
      <button onClick={logout} style={{ padding: "10px 20px", background: "#74867A", color: "#fff", border: "none", borderRadius: 8, cursor: "pointer", fontSize: 13 }}>
        Ieși din cont
      </button>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route
            path="/"
            element={
              <PrivateRoute>
                <HomePage />
              </PrivateRoute>
            }
          />
          <Route
            path="/admin"
            element={
              <AdminRoute>
                <AdminPage />
              </AdminRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}