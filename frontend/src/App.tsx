import { BrowserRouter, Routes, Route, Navigate, useNavigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import LoginPage from "./pages/login/LoginPage";
import RegisterPage from "./pages/register/RegisterPage";
import ProfilePage from "./pages/profile/ProfilePage";
import type { ReactNode } from "react";

function PrivateRoute({ children }: { children: ReactNode }) {
  const { user, loading } = useAuth();
  if (loading) return null;
  return user ? <>{children}</> : <Navigate to="/login" replace />;
}

function HomePage() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <div style={{ padding: 40, fontFamily: "'Open Sans', sans-serif", color: "#444" }}>
      <h2 style={{ color: "#74867A", marginBottom: 8 }}>Hello, {user?.name}! 🌷</h2>
      <p style={{ color: "#BDB4AC", marginBottom: 20 }}>Role: {user?.role}</p>
      <div style={{ display: "flex", gap: 12 }}>
        <button onClick={() => navigate("/profile")} style={{ padding: "10px 20px", background: "#D4888C", color: "#fff", border: "none", borderRadius: 8, cursor: "pointer", fontSize: 13 }}>
          My Account
        </button>
        <button onClick={logout} style={{ padding: "10px 20px", background: "#74867A", color: "#fff", border: "none", borderRadius: 8, cursor: "pointer", fontSize: 13 }}>
          Logout
        </button>
      </div>
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
  const navigate = useNavigate();
  return (
    <div style={{ padding: 40, fontFamily: "'Open Sans', sans-serif", color: "#444" }}>
      <h2 style={{ color: "#74867A", marginBottom: 8 }}>Admin Dashboard</h2>
      <p style={{ color: "#BDB4AC", marginBottom: 20 }}>Logged as: {user?.name}</p>
      <div style={{ display: "flex", gap: 12 }}>
        <button onClick={() => navigate("/profile")} style={{ padding: "10px 20px", background: "#D4888C", color: "#fff", border: "none", borderRadius: 8, cursor: "pointer", fontSize: 13 }}>
          My Account
        </button>
        <button onClick={logout} style={{ padding: "10px 20px", background: "#74867A", color: "#fff", border: "none", borderRadius: 8, cursor: "pointer", fontSize: 13 }}>
          Logout
        </button>
      </div>
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
          <Route path="/" element={<PrivateRoute><HomePage /></PrivateRoute>} />
          <Route path="/profile" element={<PrivateRoute><ProfilePage /></PrivateRoute>} />
          <Route path="/admin" element={<AdminRoute><AdminPage /></AdminRoute>} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}