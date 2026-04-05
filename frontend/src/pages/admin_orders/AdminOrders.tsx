import { useEffect, useState } from "react";
import React from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { getAllOrdersForAdmin, updateOrderStatus } from "../../services/orderService";
import styles from "./AdminOrders.module.css";

const STATUSES = ["pending", "confirmed", "delivered", "cancelled"];

const STATUS_LABELS: Record<string, string> = {
  pending: "Pending",
  confirmed: "Confirmed",
  delivered: "Delivered",
  cancelled: "Cancelled",
};

const TRANSITIONS: Record<string, string[]> = {
  pending: ["confirmed", "cancelled"],
  confirmed: ["delivered", "cancelled"],
  delivered: ["cancelled"],
  cancelled: [],
};

export default function AdminOrders() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const isAdmin = user?.role === "admin";

  const [orders, setOrders] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterStatus, setFilterStatus] = useState<string>("");
  const [updatingId, setUpdatingId] = useState<number | null>(null);
  const [expandedId, setExpandedId] = useState<number | null>(null);

  useEffect(() => {
    if (!isAdmin) { navigate("/"); return; }
    loadOrders();
  }, [filterStatus]);

  async function loadOrders() {
    setLoading(true);
    try {
      const data = await getAllOrdersForAdmin(filterStatus || undefined);
      setOrders(data);
    } catch {
    } finally {
      setLoading(false);
    }
  }

  async function handleStatusChange(orderId: number, newStatus: string) {
    setUpdatingId(orderId);
    try {
      const updated = await updateOrderStatus(orderId, newStatus);
      setOrders((prev) => prev.map((o) => (o.id === orderId ? updated : o)));
    } catch (err: any) {
      alert(err.message ?? "Failed to update status.");
    } finally {
      setUpdatingId(null);
    }
  }

  function toggleExpand(id: number) {
    setExpandedId((prev) => (prev === id ? null : id));
  }

  if (!isAdmin) return null;

  return (
    <main className={styles.page}>
      <div className={styles.pageHeader}>
        <h1 className={styles.title}>Order Management</h1>
        <div className={styles.filterBar}>
          <span className={styles.filterLabel}>Filter:</span>
          {["", ...STATUSES].map((s) => (
            <button
              key={s}
              className={`${styles.filterBtn} ${filterStatus === s ? styles.filterActive : ""}`}
              onClick={() => setFilterStatus(s)}
            >
              {s === "" ? "All" : STATUS_LABELS[s]}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className={styles.stateBox}>
          <div className={styles.spinner} />
          <p>Loading…</p>
        </div>
      ) : orders.length === 0 ? (
        <div className={styles.stateBox}>
          <p>No orders found.</p>
        </div>
      ) : (
        <div className={styles.tableWrapper}>
          <table className={styles.table}>
            <thead>
              <tr>
                <th>Order #</th>
                <th>Customer</th>
                <th>Phone</th>
                <th>Total</th>
                <th>Status</th>
                <th>Date</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {orders.map((order) => (
                <React.Fragment key={order.id}>
                  <tr className={expandedId === order.id ? styles.rowExpanded : ""}>
                    <td className={styles.orderNum}>{order.order_number}</td>
                    <td>
                      <div className={styles.customerName}>{order.customer_name}</div>
                      <div className={styles.customerEmail}>{order.customer_email}</div>
                    </td>
                    <td>{order.customer_phone}</td>
                    <td className={styles.total}>{Number(order.total_price).toFixed(2)} RON</td>
                    <td>
                      <select
                        className={`${styles.badge} ${styles[`badge_${order.status}`]} ${styles.badgeSelect}`}
                        value={order.status}
                        disabled={updatingId === order.id || TRANSITIONS[order.status]?.length === 0}
                        onChange={(e) => handleStatusChange(order.id, e.target.value)}
                      >
                        <option value={order.status}>{STATUS_LABELS[order.status]}</option>
                        {TRANSITIONS[order.status]?.map((s) => (
                          <option key={s} value={s}>{STATUS_LABELS[s]}</option>
                        ))}
                      </select>
                    </td>
                    <td className={styles.date}>
                      {new Date(order.created_at).toLocaleDateString("ro-RO")}
                    </td>
                    <td>
                      <button className={styles.expandBtn} onClick={() => toggleExpand(order.id)}>
                        {expandedId === order.id ? "▲" : "▼"}
                      </button>
                    </td>
                  </tr>
                  {expandedId === order.id && (
                    <tr className={styles.itemsRow}>
                      <td colSpan={7}>
                        <div className={styles.itemsBox}>
                          <p className={styles.deliveryAddress}>
                            📍 {order.delivery_address}
                            {order.card_message && (
                              <span className={styles.cardMsg}> · "{order.card_message}"</span>
                            )}
                          </p>
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