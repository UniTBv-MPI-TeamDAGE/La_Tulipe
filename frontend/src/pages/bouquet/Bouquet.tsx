import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getProducts } from "../../services/productService";
import { useCart } from "../../context/CartContext";
import styles from "./Bouquet.module.css";

export default function Bouquet() {
  const navigate = useNavigate();
  const { addBouquet } = useCart();

  const [flowers, setFlowers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selection, setSelection] = useState<{ product: any; quantity: number }[]>([]);
  const [justAdded, setJustAdded] = useState(false);

  useEffect(() => {
    getProducts({ type: "individual" })
      .then((data: any[]) => setFlowers(data.filter((p) => p.stock > 0)))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  function getQty(productId: number): number {
    return selection.find((s) => s.product.id === productId)?.quantity ?? 0;
  }

  function setQty(product: any, qty: number) {
    if (qty < 0 || qty > product.stock) return;
    setSelection((prev) => {
      if (qty === 0) return prev.filter((s) => s.product.id !== product.id);
      const exists = prev.find((s) => s.product.id === product.id);
      if (exists) return prev.map((s) => s.product.id === product.id ? { ...s, quantity: qty } : s);
      return [...prev, { product, quantity: qty }];
    });
  }

  const activeItems = selection.filter((s) => s.quantity > 0);
  const isEmpty = activeItems.length === 0;
  const totalPrice = activeItems.reduce((sum, s) => sum + s.product.price * s.quantity, 0);

  function handleAddToCart() {
    if (isEmpty) return;
    const label = "Bouquet: " + activeItems.map((s) => `${s.quantity}× ${s.product.name}`).join(", ");
    addBouquet({
      type: "bouquet",
      id: `bouquet-${Date.now()}`,
      label,
      flowers: activeItems.map((s) => ({ product: s.product, quantity: s.quantity })),
      totalPrice,
    });
    setJustAdded(true);
    setTimeout(() => { setJustAdded(false); navigate("/cart"); }, 1100);
  }

  return (
    <main className={styles.page}>
      <div className={styles.header}>
        <h1 className={styles.title}>Custom Bouquet Builder</h1>
        <p className={styles.subtitle}>Select flowers and quantities — price updates in real time.</p>
      </div>

      <div className={styles.layout}>
        <div className={styles.flowerList}>
          {loading && (
            <div className={styles.loadingRow}>
              <div className={styles.spinner} />
              <span>Loading flowers…</span>
            </div>
          )}
          {!loading && flowers.length === 0 && (
            <p className={styles.emptyState}>No individual flowers available at the moment.</p>
          )}
          {flowers.map((flower) => {
            const qty = getQty(flower.id);
            return (
              <div key={flower.id} className={`${styles.flowerRow} ${qty > 0 ? styles.flowerRowSelected : ""}`}>
                <div className={styles.flowerInfo}>
                  {flower.image_url ? (
                    <img src={flower.image_url} alt={flower.name} className={styles.flowerImg} loading="lazy" />
                  ) : (
                    <div className={styles.flowerImgFallback}>🌸</div>
                  )}
                  <div className={styles.flowerText}>
                    <p className={styles.flowerName}>{flower.name}</p>
                    <p className={styles.flowerMeta}>{flower.price.toFixed(2)} RON / stem · {flower.stock} available</p>
                    {flower.colors.length > 0 && (
                      <div className={styles.flowerColors}>
                        {flower.colors.map((c: any) => (
                          <span key={c.id} className={styles.colorDot} style={{ background: c.hex_code ?? "#ccc" }} title={c.name} />
                        ))}
                      </div>
                    )}
                  </div>
                </div>
                <div className={styles.qtyControl}>
                  <button className={styles.qtyBtn} onClick={() => setQty(flower, qty - 1)} disabled={qty === 0}>−</button>
                  <span className={styles.qtyValue}>{qty}</span>
                  <button className={styles.qtyBtn} onClick={() => setQty(flower, qty + 1)} disabled={qty >= flower.stock}>+</button>
                </div>
              </div>
            );
          })}
        </div>

        <aside className={styles.summary}>
          <h2 className={styles.summaryTitle}>Your bouquet</h2>
          {isEmpty ? (
            <p className={styles.summaryEmpty}>Select flowers on the left to build your bouquet.</p>
          ) : (
            <ul className={styles.summaryList}>
              {activeItems.map((s) => (
                <li key={s.product.id} className={styles.summaryRow}>
                  <span>{s.quantity}× {s.product.name}</span>
                  <span className={styles.summaryPrice}>{(s.product.price * s.quantity).toFixed(2)} RON</span>
                </li>
              ))}
            </ul>
          )}
          {!isEmpty && (
            <div className={styles.totalRow}>
              <span>Total</span>
              <strong>{totalPrice.toFixed(2)} RON</strong>
            </div>
          )}
          <button className={styles.addBtn} onClick={handleAddToCart} disabled={isEmpty}>
            {justAdded ? "✓ Added to cart!" : "Add bouquet to cart"}
          </button>
          <button className={styles.clearBtn} onClick={() => setSelection([])} disabled={isEmpty}>
            Clear selection
          </button>
        </aside>
      </div>
    </main>
  );
}