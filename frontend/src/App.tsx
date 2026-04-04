import { BrowserRouter, Routes, Route, Navigate, useLocation } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import { CartProvider } from "./context/CartContext";
import LoginPage from "./pages/login/LoginPage";
import RegisterPage from "./pages/register/RegisterPage";
import ProfilePage from "./pages/profile/ProfilePage";
import Navbar from "./components/shared/navbar/Navbar";
import Footer from "./components/shared/footer/Footer";
import Home from "./pages/home/HomePage";
import ProductDetail from "./pages/product_detail/ProductDetail";
import Bouquet from "./pages/bouquet/Bouquet";
import AdminProducts from "./pages/admin_products/AdminProducts";
import CartPage from "./pages/cart/CartPage";
import CheckoutPage from "./pages/checkout/CheckoutPage";
import OrdersPage from "./pages/orders/OrdersPage";
import type { ReactNode } from "react";

function PrivateRoute({ children }: { children: ReactNode }) {
  const { user, loading } = useAuth();
  if (loading) return null;
  return user ? <>{children}</> : <Navigate to="/login" replace />;
}

function AdminRoute({ children }: { children: ReactNode }) {
  const { user, loading } = useAuth();
  if (loading) return null;
  if (!user) return <Navigate to="/login" replace />;
  if (user.role !== "admin") return <Navigate to="/" replace />;
  return <>{children}</>;
}

function AppShell() {
  const location = useLocation();
  const authPages = ["/login", "/register"];
  const isAuthPage = authPages.includes(location.pathname);

  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      {!isAuthPage && <Navbar />}
      <div style={{ flex: 1 }}>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/" element={<PrivateRoute><Home /></PrivateRoute>} />
          <Route path="/products/:id" element={<PrivateRoute><ProductDetail /></PrivateRoute>} />
          <Route path="/bouquet" element={<PrivateRoute><Bouquet /></PrivateRoute>} />
          <Route path="/cart" element={<PrivateRoute><CartPage /></PrivateRoute>} />
          <Route path="/checkout" element={<PrivateRoute><CheckoutPage /></PrivateRoute>} />
          <Route path="/profile" element={<PrivateRoute><ProfilePage /></PrivateRoute>} />
          <Route path="/profile/orders" element={<PrivateRoute><OrdersPage /></PrivateRoute>} />
          <Route path="/admin" element={<AdminRoute><AdminProducts /></AdminRoute>} />
          <Route path="/admin/products" element={<AdminRoute><AdminProducts /></AdminRoute>} />
        </Routes>
      </div>
      <Footer />
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <CartProvider>
          <AppShell />
        </CartProvider>
      </BrowserRouter>
    </AuthProvider>
  );
}