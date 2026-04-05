import { Link } from "react-router-dom";
import styles from "./Footer.module.css";
import logo from "../../../assets/logo_flower.png";

export default function Footer() {
  return (
    <footer className={styles.footer}>
      <div className={styles.container}>
        <div className={styles.brand}>
  <img src={logo} alt="La Tulipe" className={styles.brandLogo} />
</div>

        <div className={styles.col}>
          <p className={styles.colTitle}>Shop</p>
          <Link to="/" className={styles.colLink}>All flowers</Link>
          <Link to="/bouquet" className={styles.colLink}>Build a bouquet</Link>
        </div>

        <div className={styles.col}>
          <p className={styles.colTitle}>Account</p>
          <Link to="/profile" className={styles.colLink}>My profile</Link>
          <Link to="/orders" className={styles.colLink}>My orders</Link>
        </div>

        <div className={styles.col}>
          <p className={styles.colTitle}>Contact</p>
          <a href="tel:+40123456789" className={styles.colLink}>📞 +40 123 456 789</a>
          <a href="mailto:contact@latulipe.ro" className={styles.colLink}>✉️ contact@latulipe.ro</a>
          <p className={styles.colLink}>📍 Strada Florilor 10, Brașov</p>
        </div>

        <div className={styles.col}>
          <p className={styles.colTitle}>Hours</p>
          <p className={styles.colText}>Mon – Fri: 8:00 – 19:00</p>
          <p className={styles.colText}>Saturday: 9:00 – 17:00</p>
          <p className={styles.colText}>Sunday: 10:00 – 15:00</p>
        </div>
      </div>

      <div className={styles.bottom}>
        <p>© {new Date().getFullYear()} La Tulipe. All rights reserved.</p>
      </div>
    </footer>
  );
}