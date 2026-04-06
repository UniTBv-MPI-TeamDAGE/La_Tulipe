import { useState, useEffect, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { getUserMe, updateUserMe } from "../../services/authService";
import type { UserMeResponse } from "../../dtos/auth";
import styles from "./ProfilePage.module.css";

export default function ProfilePage() {
  const { updateUser } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState<UserMeResponse>({ name: "", email: "", phone: "" });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    getUserMe()
      .then((data) => {
        console.log("USER ME:", data);  
        setForm(data);
      })
      .catch((err) => {
        console.log("getUserMe ERROR:", err);  
        navigate("/login");
      })
      .finally(() => setLoading(false));
  }, [navigate]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess(false);
    setSaving(true);
    try {
      const updated = await updateUserMe({ name: form.name, phone: form.phone });
      updateUser({ name: updated.name, phone: updated.phone });
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
    } catch {
      setError("Error saving data. Try again.");
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <p>Loading...</p>;

  return (
    <div className={styles.page}>
      <div className={styles.card}>
        <header className={styles.header}>
          <h1 className={styles.title}>My Account</h1>
        </header>
        <form onSubmit={handleSubmit} className={styles.form}>

          <div className={styles.field}>
            <label className={styles.label}>Name</label>
            <input
              className={styles.input}
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              placeholder="Full name"
            />
          </div>

          <div className={styles.field}>
            <label className={styles.label}>Email</label>
            <input className={styles.input} value={form.email} disabled />
          </div>

          <div className={styles.field}>
            <label className={styles.label}>Phone</label>
            <input
              className={styles.input}
              value={form.phone ?? ""}
              onChange={(e) => setForm({ ...form, phone: e.target.value })}
              placeholder="07xx xxx xxx"
            />
          </div>

          {success && <p style={{ color: "#74867A", fontSize: 13 }}>✓ Data updated successfully!</p>}
          {error && <p style={{ color: "#b43c28", fontSize: 13 }}>{error}</p>}

          <button type="submit" className={styles.btnPrimary} disabled={saving}>
            {saving ? "Saving..." : "Save changes"}
          </button>
        </form>
      </div>
    </div>
  );
}