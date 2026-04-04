import { useState, type FormEvent, type ChangeEvent } from "react";
import { useNavigate, Link } from "react-router-dom";
import { registerUser } from "../../services/authService";
import type { RegisterRequest } from "../../dtos/auth";
import styles from "./RegisterPage.module.css";
import logo from "../../assets/logo_slogan.png";

interface FormErrors {
  name?: string;
  email?: string;
  password?: string;
  confirm_password?: string;
  admin_code?:string;
  general?: string;
}

export default function RegisterPage() {
  const navigate = useNavigate();

  const [form, setForm] = useState<RegisterRequest>({
    name: "",
    email: "",
    password: "",
    confirm_password: "",
    phone: "",
    role: "customer",   
    admin_code: "", 
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [loading, setLoading] = useState(false);

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    if (errors[name as keyof FormErrors]) {
      setErrors((prev) => ({ ...prev, [name]: undefined }));
    }
  };

  const validate = (): FormErrors => {
    const errs: FormErrors = {};
    if (!form.name.trim()) errs.name = "Name required";
    if (!form.email.trim()) errs.email = "Email required";
    if (form.password.length < 8)
      errs.password = "Password must have at least 8 characters";
    if (form.password !== form.confirm_password)
      errs.confirm_password = "Passwords don't match";
    if (form.role === "admin" && !form.admin_code)
    {    errs.admin_code = "Admin code is required";}

    return errs;
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    const validationErrors = validate();
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }
    setLoading(true);
    try {
      await registerUser(form);
      navigate("/");
    } catch (err: unknown) {
      const apiErr = err as { status: number; detail: string };
      if (apiErr.status === 409) {
        setErrors({ email: "Email already used" });
      } else if (apiErr.status === 400) {
        const msg = apiErr.detail ?? "Invalid data";
        if (msg.toLowerCase().includes("password")) {
          setErrors({ password: msg });
        } else {
          setErrors({ general: msg });
        }
      } else if (apiErr.status === 403) {
        setErrors({ admin_code: "Invalid admin code" });}
      
      else {
        setErrors({ general: "Couldn't connect to the server" });
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
              <div className={styles.errorBanner} role="alert">{errors.general}</div>
            )}

            <div className={styles.field}>
              <label className={styles.label} htmlFor="reg-name">Full name</label>
              <input id="reg-name" name="name" type="text" autoComplete="name"
                value={form.name} onChange={handleChange} placeholder="Ana Popescu"
                className={`${styles.input} ${errors.name ? styles.inputError : ""}`} />
              {errors.name && <span className={styles.fieldError} role="alert">{errors.name}</span>}
            </div>

            <div className={styles.field}>
              <label className={styles.label} htmlFor="reg-email">Email adress</label>
              <input id="reg-email" name="email" type="email" autoComplete="email"
                value={form.email} onChange={handleChange} placeholder="ana@example.com"
                className={`${styles.input} ${errors.email ? styles.inputError : ""}`} />
              {errors.email && <span className={styles.fieldError} role="alert">{errors.email}</span>}
            </div>

            <div className={styles.field}>
              <label className={styles.label} htmlFor="reg-phone">
                Phone <span className={styles.optional}>(optional)</span>
              </label>
              <input id="reg-phone" name="phone" type="tel" autoComplete="tel"
                value={form.phone} onChange={handleChange} placeholder="07xx xxx xxx"
                className={styles.input} />
            </div>

            <div className={styles.field}>
              <label className={styles.label} htmlFor="reg-role">Account type</label>
              <select
                id="reg-role"
                name="role"
                value={form.role}
                onChange={(e) => {
                  setForm((prev) => ({ ...prev, role: e.target.value as "customer" | "admin", admin_code: "" }));
                  setErrors((prev) => ({ ...prev, admin_code: undefined }));
                }}
                className={styles.input}
              >
                <option value="customer">Customer</option>
                <option value="admin">Administrator</option>
              </select>
            </div>

            {form.role === "admin" && (
              <div className={styles.field}>
                <label className={styles.label} htmlFor="reg-admincode">Admin secret code</label>
                <input
                  id="reg-admincode"
                  name="admin_code"
                  type="password"
                  value={form.admin_code}
                  onChange={handleChange}
                  placeholder="Enter admin code"
                  className={`${styles.input} ${errors.admin_code ? styles.inputError : ""}`}
                />
                {errors.admin_code && (
                  <span className={styles.fieldError} role="alert">{errors.admin_code}</span>
                )}
              </div>
            )}

            <div className={styles.row}>
              <div className={styles.field}>
                <label className={styles.label} htmlFor="reg-password">Password</label>
                <input id="reg-password" name="password" type="password" autoComplete="new-password"
                  value={form.password} onChange={handleChange} placeholder="Min. 8 characters"
                  className={`${styles.input} ${errors.password ? styles.inputError : ""}`} />
                {errors.password && <span className={styles.fieldError} role="alert">{errors.password}</span>}
              </div>

              <div className={styles.field}>
                <label className={styles.label} htmlFor="reg-confirm">Confirmation</label>
                <input id="reg-confirm" name="confirm_password" type="password" autoComplete="new-password"
                  value={form.confirm_password} onChange={handleChange} placeholder="Re-enter password "
                  className={`${styles.input} ${errors.confirm_password ? styles.inputError : ""}`} />
                {errors.confirm_password && <span className={styles.fieldError} role="alert">{errors.confirm_password}</span>}
              </div>
            </div>

            <button type="submit" className={styles.btnPrimary} disabled={loading}>
              {loading ? <><span className={styles.spinner} /> Processing...</> : "Register"}
            </button>
          </form>

          <p className={styles.footer}>
            Already have an account?{" "}
            <Link to="/login" className={styles.link}>Login</Link>
          </p>
        </div>
      </main>
    </div>
  );
}