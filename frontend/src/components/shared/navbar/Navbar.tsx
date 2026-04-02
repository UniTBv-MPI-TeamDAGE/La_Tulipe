import { useRef, useState, useEffect } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { useAuth } from "../../../context/AuthContext";
import { useCart } from "../../../context/CartContext";
import styles from "./Navbar.module.css";
import logo from "../../../assets/logo_slogan.png";

export default function Navbar() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { user, logout } = useAuth();
  const { totalItems } = useCart();

  const [searchValue, setSearchValue] = useState(
    () => searchParams.get("search") ?? ""
  );
  const [menuOpen, setMenuOpen] = useState(false);
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    setSearchValue(searchParams.get("search") ?? "");
  }, [searchParams]);

  function handleSearchChange(e: React.ChangeEvent<HTMLInputElement>) {
    const val = e.target.value;
    setSearchValue(val);
    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => {
      const next = new URLSearchParams(window.location.search);
      if (val.length >= 2) next.set("search", val);
      else next.delete("search");
      navigate(`/?${next.toString()}`);
    }, 300);
  }

  function handleLogout() {
    logout();
    navigate("/login");
    setMenuOpen(false);
  }

  const isAdmin = user?.role === "admin";

  return (
    <header className={styles.header}>
      <nav className={styles.nav}>
        <Link to="/" className={styles.logoLink} onClick={() => setMenuOpen(false)}>
         <img src={logo} alt="La Tulipe" className={styles.logoImg} />
        </Link>

        <div className={styles.searchWrapper}>
          <span className={styles.searchIcon}>🔍</span>
          <input
            className={styles.searchInput}
            type="search"
            placeholder="Search flowers…"
            value={searchValue}
            onChange={handleSearchChange}
          />
        </div>

        <div className={styles.actions}>
          <Link to="/bouquet" className={styles.navLink}>
            🌺 Build bouquet
          </Link>
          {isAdmin && (
            <Link to="/admin/products" className={styles.adminLink}>
              ⚙️ Admin
            </Link>
          )}
          <Link to="/cart" className={styles.cartBtn} aria-label="Cart">
            🛒
            {totalItems > 0 && (
              <span className={styles.badge}>{totalItems}</span>
            )}
          </Link>
          {user ? (
            <div className={styles.userMenu}>
              <Link to="/profile" className={styles.navLink}>
                👤 {user.name}
              </Link>
              <button className={styles.logoutBtn} onClick={handleLogout}>
                Sign out
              </button>
            </div>
          ) : (
            <Link to="/login" className={styles.loginBtn}>
              Sign in
            </Link>
          )}
        </div>

        <button
          className={styles.hamburger}
          onClick={() => setMenuOpen((o) => !o)}
          aria-label="Toggle menu"
        >
          <span className={styles.bar} style={{ transform: menuOpen ? "rotate(45deg) translate(5px,5px)" : "none" }} />
          <span className={styles.bar} style={{ opacity: menuOpen ? 0 : 1 }} />
          <span className={styles.bar} style={{ transform: menuOpen ? "rotate(-45deg) translate(5px,-5px)" : "none" }} />
        </button>
      </nav>

      {menuOpen && (
        <div className={styles.mobileMenu}>
          <div className={styles.mobileSearchWrapper}>
            <span className={styles.searchIcon}>🔍</span>
            <input
              className={styles.searchInput}
              type="search"
              placeholder="Search flowers…"
              value={searchValue}
              onChange={handleSearchChange}
            />
          </div>
          <Link to="/bouquet" className={styles.mobileLink} onClick={() => setMenuOpen(false)}>
            🌺 Build bouquet
          </Link>
          <Link to="/cart" className={styles.mobileLink} onClick={() => setMenuOpen(false)}>
            🛒 Cart
            {totalItems > 0 && <span className={styles.mobileBadge}>{totalItems}</span>}
          </Link>
          {isAdmin && (
            <Link to="/admin/products" className={styles.mobileLink} onClick={() => setMenuOpen(false)}>
              ⚙️ Admin panel
            </Link>
          )}
          {user ? (
            <>
              <Link to="/profile" className={styles.mobileLink} onClick={() => setMenuOpen(false)}>
                👤 {user.name}
              </Link>
              <button className={styles.mobileLogout} onClick={handleLogout}>
                Sign out
              </button>
            </>
          ) : (
            <Link to="/login" className={styles.mobileLink} onClick={() => setMenuOpen(false)}>
              Sign in
            </Link>
          )}
        </div>
      )}
    </header>
  );
}