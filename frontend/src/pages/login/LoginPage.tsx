import { useState, type FormEvent, type ChangeEvent } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { loginUser, getUserMe } from "../../services/authService";
import styles from "./LoginPage.module.css";
import logo from "../../assets/logo_slogan.png";

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
    <div className="authPage">
      <main className={styles.page}>
        <div className={styles.logoFixed}>
          <img src={logo} alt="La Tulipe" />
        </div>
        <div className={styles.card}>
          <form onSubmit={handleSubmit} noValidate className={styles.form}>
            {errors.general && (
              <div className={styles.errorBanner} role="alert">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
                  <circle cx="12" cy="12" r="10" /><line x1="12" y1="8" x2="12" y2="12" /><line x1="12" y1="16" x2="12.01" y2="16" />
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
      </main>
    </div>
  );
}