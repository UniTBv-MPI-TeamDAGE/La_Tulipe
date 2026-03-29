import { useState, type FormEvent, type ChangeEvent } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { loginUser, getUserMe } from "../../services/authService";
import styles from "./LoginPage.module.css";

interface FormErrors {
  email?: string;
  password?: string;
  general?: string;
}

export default function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [form, setForm] = useState({ email: "", password: "" });
  const [errors, setErrors] = useState<FormErrors>({});
  const [loading, setLoading] = useState(false);

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    if (errors.general || errors[name as keyof FormErrors]) {
      setErrors({});
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    const errs: FormErrors = {};
    if (!form.email.trim()) errs.email = "Email required";
    if (!form.password) errs.password = "Password required";
    if (Object.keys(errs).length > 0) { setErrors(errs); return; }

    setLoading(true);
    try {
      const data = await loginUser(form);
      console.log("LOGIN RESPONSE:", data);

      let name = data.name;
      if (!name) {
        const me = await getUserMe(data.access_token);
        name = me.name;
      }

      login({ ...data, name, email: form.email });

      if (data.role === "admin") {
        navigate("/admin");
      } else {
        navigate("/");
      }
    } catch (err: unknown) {
      const apiErr = err as { status: number; detail: string };
      if (apiErr.status === 401) {
        setErrors({ general: "Incorrect email or password" });
      } else {
        setErrors({ general: "Could not connect to the server" });
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.page}>
      <div className={styles.card}>
        <header className={styles.header}>
          <div className={styles.logo}>
            <span className={styles.logoText}>La Tulipe</span>
            <svg className={styles.logoIcon} viewBox="0 0 30 60" fill="none" aria-hidden="true">
              <path d="M15 20 C15 20, 10 14, 10 8 C10 3, 14 0, 15 0 C16 0, 20 3, 20 8 C20 14, 15 20, 15 20Z" fill="#D4888C"/>
              <path d="M15 22 C15 22, 8 17, 6 11 C4 6, 7 2, 9 1 C11 0, 14 4, 15 8 C13 4, 10 2, 9 3 C7 4, 6 8, 8 12 C10 16, 15 22, 15 22Z" fill="#D4888C" opacity="0.65"/>
              <path d="M15 22 C15 22, 22 17, 24 11 C26 6, 23 2, 21 1 C19 0, 16 4, 15 8 C17 4, 20 2, 21 3 C23 4, 24 8, 22 12 C20 16, 15 22, 15 22Z" fill="#D4888C" opacity="0.65"/>
              <line x1="15" y1="20" x2="15" y2="58" stroke="#D4888C" strokeWidth="1.5" strokeLinecap="round"/>
              <path d="M15 38 C15 38, 10 33, 8 36 C8 36, 11 37, 15 38Z" fill="#D4888C" opacity="0.6"/>
              <path d="M15 44 C15 44, 20 39, 22 42 C22 42, 19 43, 15 44Z" fill="#D4888C" opacity="0.6"/>
            </svg>
          </div>
          <h1 className={styles.title}>Bloom with us</h1>
        </header>

        <form onSubmit={handleSubmit} noValidate className={styles.form}>
          {errors.general && (
            <div className={styles.errorBanner} role="alert">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
                <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
              </svg>
              {errors.general}
            </div>
          )}

          <div className={styles.field}>
            <label className={styles.label} htmlFor="login-email">Email</label>
            <input id="login-email" name="email" type="email" autoComplete="email"
              value={form.email} onChange={handleChange} placeholder="address@example.com"
              className={`${styles.input} ${errors.email ? styles.inputError : ""}`} />
            {errors.email && <span className={styles.fieldError} role="alert">{errors.email}</span>}
          </div>

          <div className={styles.field}>
            <label className={styles.label} htmlFor="login-password">Password</label>
            <input id="login-password" name="password" type="password" autoComplete="current-password"
              value={form.password} onChange={handleChange} placeholder="Your password"
              className={`${styles.input} ${errors.password ? styles.inputError : ""}`} />
            {errors.password && <span className={styles.fieldError} role="alert">{errors.password}</span>}
          </div>

          <button type="submit" className={styles.btnPrimary} disabled={loading}>
            {loading ? <><span className={styles.spinner} /> Verifying...</> : "Login"}
          </button>

          <button type="button" className={styles.btnSecondary} onClick={() => navigate("/register")}>
            Register
          </button>
        </form>
      </div>
    </div>
  );
}