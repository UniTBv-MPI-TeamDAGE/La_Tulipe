import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getMyOrders, getMyOrderById } from "../../services/orderService";
import styles from "./OrdersPage.module.css";

const STATUS_CONFIG: Record<string, { label: string; className: string }> = {
  pending:   { label: "Pending",   className: "badgePending" },
  confirmed: { label: "Confirmed", className: "badgeConfirmed" },
  delivered: { label: "Delivered", className: "badgeDelivered" },
  cancelled: { label: "Cancelled", className: "badgeCancelled" },
};

export default function OrdersPage() {
  const navigate = useNavigate();
  const [orders, setOrders] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedOrder, setSelectedOrder] = useState<any>(null);
  const [detailLoading, setDetailLoading] = useState(false);

  useEffect(() => {
    getMyOrders()
      .then(setOrders)
      .catch((err: any) => {
        if (err.status === 401) navigate("/login");
        else setError("Failed to load orders.");
      })
      .finally(() => setLoading(false));
  }, []);

  async function openOrder(id: number) {
    setDetailLoading(true);
    try {
      const order = await getMyOrderById(id);
      setSelectedOrder(order);
    } catch {
      //
    } finally {
      setDetailLoading(false);
    }
  }

  if (loading) {
    return (
      <main className={styles.page}>
        <div className={styles.center}>
          <div className={styles.spinner} />
        </div>
      </main>
    );
  }

  if (error) {
    return (
      <main className={styles.page}>
        <p className={styles.errorText}>{error}</p>
      </main>
    );
  }

  if (selectedOrder) {
    const cfg = STATUS_CONFIG[selectedOrder.status] ?? { label: selectedOrder.status, className: "badgePending" };
    return (
      <main className={styles.page}>
        <button className={styles.backLink} onClick={() => setSelectedOrder(null)}>
          ← Back to orders
        </button>
        <div className={styles.detailCard}>
          <div className={styles.detailHeader}>
            <div>
              <h2 className={styles.orderNumber}>{selectedOrder.order_number}</h2>
              <p className={styles.orderDate}>
                {new Date(selectedOrder.created_at).toLocaleDateString("ro-RO", {
                  year: "numeric", month: "long", day: "numeric",
                })}
              </p>
            </div>
            <span className={`${styles.badge} ${styles[cfg.className]}`}>{cfg.label}</span>
          </div>

          <div className={styles.detailSection}>
            <h3 className={styles.detailSectionTitle}>Items</h3>
            {selectedOrder.items.map((item: any) => (
              <div key={item.id} className={styles.detailItem}>
                <span className={styles.detailItemName}>
                  {item.product_name ?? "Custom Bouquet"}
                  {item.color_name && ` — ${item.color_name}`}
                </span>
                <span className={styles.detailItemQty}>×{item.quantity}</span>
                <span className={styles.detailItemPrice}>{item.line_total.toFixed(2)} RON</span>
              </div>
            ))}
            <div className={styles.detailTotal}>
              <span>Total</span>
              <strong>{selectedOrder.total_price.toFixed(2)} RON</strong>
            </div>
          </div>

          <div className={styles.detailSection}>
            <h3 className={styles.detailSectionTitle}>Delivery</h3>
            <p className={styles.detailMeta}>{selectedOrder.customer_name}</p>
            <p className={styles.detailMeta}>{selectedOrder.customer_phone}</p>
            <p className={styles.detailMeta}>{selectedOrder.delivery_address}</p>
            {selectedOrder.card_message && (
              <p className={styles.detailMessage}>"{selectedOrder.card_message}"</p>
            )}
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className={styles.page}>
      <h1 className={styles.title}>My orders</h1>

      {orders.length === 0 ? (
        <div className={styles.empty}>
          <p>You haven't placed any orders yet.</p>
          <button className={styles.catalogBtn} onClick={() => navigate("/")}>
            Discover our flowers
          </button>
        </div>
      ) : (
        <div className={styles.orderList}>
          {orders.map((order: any) => {
            const cfg = STATUS_CONFIG[order.status] ?? { label: order.status, className: "badgePending" };
            return (
              <button
                key={order.id}
                className={styles.orderCard}
                onClick={() => openOrder(order.id)}
                disabled={detailLoading}
              >
                <div className={styles.orderCardLeft}>
                  <p className={styles.orderCardNumber}>{order.order_number}</p>
                  <p className={styles.orderCardDate}>
                    {new Date(order.created_at).toLocaleDateString("ro-RO", {
                      year: "numeric", month: "short", day: "numeric",
                    })}
                  </p>
                  <p className={styles.orderCardItems}>
                    {order.items.length} item{order.items.length !== 1 ? "s" : ""}
                  </p>
                </div>
                <div className={styles.orderCardRight}>
                  <span className={`${styles.badge} ${styles[cfg.className]}`}>{cfg.label}</span>
                  <p className={styles.orderCardTotal}>{order.total_price.toFixed(2)} RON</p>
                </div>
              </button>
            );
          })}
        </div>
      )}
    </main>
  );
}