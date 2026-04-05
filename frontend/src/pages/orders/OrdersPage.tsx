import { useEffect, useState } from "react";
import React from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { getMyOrders } from "../../services/orderService";
import styles from "./OrdersPage.module.css";

const STATUS_LABELS: Record<string, string> = {
  pending: "Pending",
  confirmed: "Confirmed",
  delivered: "Delivered",
  cancelled: "Cancelled",
};

export default function OrdersPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [orders, setOrders] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [expandedId, setExpandedId] = useState<number | null>(null);

  useEffect(() => {
    if (!user) { navigate("/login"); return; }
    getMyOrders()
      .then(setOrders)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <main className={styles.page}>
      <h1 className={styles.title}>My Orders</h1>

      {loading ? (
        <div className={styles.stateBox}>
          <div className={styles.spinner} />
          <p>Loading…</p>
        </div>
      ) : orders.length === 0 ? (
        <div className={styles.stateBox}>
          <p>You have no orders yet.</p>
        </div>
      ) : (
        <div className={styles.tableWrapper}>
          <table className={styles.table}>
            <thead>
              <tr>
                <th>Order #</th>
                <th>Total</th>
                <th>Status</th>
                <th>Date</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {orders.map((order) => (
                <React.Fragment key={order.id}>
                  <tr>
                    <td className={styles.orderNum}>{order.order_number}</td>
                    <td className={styles.total}>{Number(order.total_price).toFixed(2)} RON</td>
                    <td>
                      <span className={`${styles.badge} ${styles[`badge_${order.status}`]}`}>
                        {STATUS_LABELS[order.status] ?? order.status}
                      </span>
                    </td>
                    <td className={styles.date}>
                      {new Date(order.created_at).toLocaleDateString("ro-RO")}
                    </td>
                    <td>
                      <button
                        className={styles.expandBtn}
                        onClick={() => setExpandedId((p) => (p === order.id ? null : order.id))}
                      >
                        {expandedId === order.id ? "▲" : "▼"}
                      </button>
                    </td>
                  </tr>
                  {expandedId === order.id && (
                    <tr className={styles.itemsRow}>
                      <td colSpan={5}>
                        <div className={styles.itemsBox}>
                          <p className={styles.deliveryAddress}>📍 {order.delivery_address}</p>
                          {order.card_message && (
                            <p className={styles.cardMsg}>💌 "{order.card_message}"</p>
                          )}
                          <table className={styles.itemsTable}>
                            <thead>
                              <tr>
                                <th>Product</th>
                                <th>Color</th>
                                <th>Qty</th>
                                <th>Unit price</th>
                                <th>Line total</th>
                              </tr>
                            </thead>
                            <tbody>
                              {order.items.map((item: any) => (
                                <tr key={item.id}>
                                  <td>{item.product_name}</td>
                                  <td>{item.color_name ?? "—"}</td>
                                  <td>{item.quantity}</td>
                                  <td>{Number(item.unit_price).toFixed(2)} RON</td>
                                  <td>{Number(item.line_total).toFixed(2)} RON</td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </main>
  );
}