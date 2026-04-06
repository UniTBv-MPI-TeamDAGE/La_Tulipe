import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useCart } from "../../context/CartContext";
import { createOrder } from "../../services/orderService";
import { useAuth } from "../../context/AuthContext";
import styles from "./CheckoutPage.module.css";

interface FormState {
  customer_name: string;
  customer_email: string;
  customer_phone: string;
  delivery_address: string;
  card_message: string;
}

export default function CheckoutPage() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const { items, totalPrice, toOrderItems, clearCart } = useCart();

  const [form, setForm] = useState<FormState>({
    customer_name: user?.name ?? "",
    customer_email: user?.email ?? "",
    customer_phone: "",
    delivery_address: "",
    card_message: "",
  });
  const [errors, setErrors] = useState<Partial<FormState>>({});
  const [submitting, setSubmitting] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);
  const [confirmedOrder, setConfirmedOrder] = useState<any>(null);

  if (items.length === 0 && !confirmedOrder) {
    return (
      <main className={styles.page}>
        <div className={styles.empty}>
          <p>Your cart is empty.</p>
          <button className={styles.backBtn} onClick={() => navigate("/")}>Go to catalog</button>
        </div>
      </main>
    );
  }

  if (confirmedOrder) {
    return (
      <main className={styles.page}>
        <div className={styles.confirmation}>
          <div className={styles.confirmIcon}>✅</div>
          <h1 className={styles.confirmTitle}>Order placed!</h1>
          <p className={styles.confirmNumber}>
            Order number: <strong>{confirmedOrder.order_number}</strong>
          </p>
          <p className={styles.confirmText}>
            Thank you, {confirmedOrder.customer_name}! We'll prepare your flowers with care.
          </p>
          <div className={styles.confirmActions}>
            <button className={styles.ordersBtn} onClick={() => navigate("/orders")}>
              View my orders
            </button>
            <button className={styles.homeBtn} onClick={() => navigate("/")}>
              Back to catalog
            </button>
          </div>
        </div>
      </main>
    );
  }

  function validate(): boolean {
    const errs: Partial<FormState> = {};
    if (!form.customer_name.trim()) errs.customer_name = "Name is required.";
    if (!form.customer_email.trim()) errs.customer_email = "Email is required.";
    else if (!/^\S+@\S+\.\S+$/.test(form.customer_email)) errs.customer_email = "Invalid email.";
    if (!form.customer_phone.trim()) errs.customer_phone = "Phone is required.";
    if (!form.delivery_address.trim()) errs.delivery_address = "Delivery address is required.";
    setErrors(errs);
    return Object.keys(errs).length === 0;
  }

  async function handleSubmit() {
    if (!validate()) return;
    setSubmitting(true);
    setApiError(null);
    try {
      const order = await createOrder({
        customer_name: form.customer_name,
        customer_email: form.customer_email,
        customer_phone: form.customer_phone,
        delivery_address: form.delivery_address,
        card_message: form.card_message.trim() || null,
        items: toOrderItems(),
      });
      clearCart();
      setConfirmedOrder(order);
    } catch (err: any) {
      if (err.status === 409) {
        setApiError("Some items are out of stock. Please review your cart.");
      } else {
        setApiError(err.message ?? "Failed to place order. Please try again.");
      }
    } finally {
      setSubmitting(false);
    }
  }

  function field(key: keyof FormState, label: string, type = "text", placeholder = "") {
    return (
      <div className={styles.field}>
        <label className={styles.label}>{label}</label>
        <input
          className={`${styles.input} ${errors[key] ? styles.inputError : ""}`}
          type={type}
          placeholder={placeholder}
          value={form[key]}
          onChange={(e) => {
            setForm((f) => ({ ...f, [key]: e.target.value }));
            if (errors[key]) setErrors((er) => ({ ...er, [key]: undefined }));
          }}
        />
        {errors[key] && <p className={styles.fieldError}>{errors[key]}</p>}
      </div>
    );
  }

  return (
    <main className={styles.page}>
      <h1 className={styles.title}>Checkout</h1>

      <div className={styles.layout}>
        <div className={styles.formSection}>
          <h2 className={styles.sectionTitle}>Delivery details</h2>

          {field("customer_name", "Full name *", "text", "e.g. Ana Popescu")}
          {field("customer_email", "Email *", "email", "e.g. ana@example.com")}
          {field("customer_phone", "Phone *", "tel", "e.g. 0721 000 000")}
          {field("delivery_address", "Delivery address *", "text", "Street, city, postal code")}

          <div className={styles.field}>
            <label className={styles.label}>Message on card <span className={styles.optional}>(optional)</span></label>
            <textarea
              className={styles.textarea}
              rows={3}
              placeholder="e.g. Happy Birthday!"
              value={form.card_message}
              onChange={(e) => setForm((f) => ({ ...f, card_message: e.target.value }))}
            />
          </div>

          {apiError && <p className={styles.apiError}>⚠️ {apiError}</p>}

          <button
            className={styles.submitBtn}
            onClick={handleSubmit}
            disabled={submitting}
          >
            {submitting ? "Placing order…" : `Place order · ${totalPrice.toFixed(2)} RON`}
          </button>
        </div>

        <aside className={styles.orderSummary}>
          <h2 className={styles.sectionTitle}>Your order</h2>
          <div className={styles.orderItems}>
            {items.map((item) => {
              if (item.type === "bouquet") {
                return (
                  <div key={item.id} className={styles.orderItem}>
                    <span className={styles.orderItemName}>{item.label}</span>
                    <span className={styles.orderItemPrice}>{item.totalPrice.toFixed(2)} RON</span>
                  </div>
                );
              }
              return (
                <div key={item.cartKey} className={styles.orderItem}>
                  <span className={styles.orderItemName}>
                    {item.quantity}× {item.product.name}
                    {item.selectedColor && ` (${item.selectedColor.name})`}
                  </span>
                  <span className={styles.orderItemPrice}>
                    {(item.product.price * item.quantity).toFixed(2)} RON
                  </span>
                </div>
              );
            })}
          </div>
          <div className={styles.orderTotal}>
            <span>Total</span>
            <strong>{totalPrice.toFixed(2)} RON</strong>
          </div>
        </aside>
      </div>
    </main>
  );
}