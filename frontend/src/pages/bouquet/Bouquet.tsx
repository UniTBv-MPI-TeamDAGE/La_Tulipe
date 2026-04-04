import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getProducts } from "../../services/productService";
import { useCart } from "../../context/CartContext";
import styles from "./Bouquet.module.css";

interface FlowerSelection {
  product: any;
  quantity: number;
  colorId?: number;
  colorName?: string;
}

export default function Bouquet() {
  const navigate = useNavigate();
  const { addBouquet } = useCart();

  const [flowers, setFlowers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selection, setSelection] = useState<FlowerSelection[]>([]);
  const [justAdded, setJustAdded] = useState(false);
  const [colorError, setColorError] = useState<string | null>(null);

  useEffect(() => {
    getProducts({ type: "individual" })
      .then((data: any[]) => setFlowers(data.filter((p) => p.stock > 0)))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  function getSelection(productId: number): FlowerSelection | undefined {
    return selection.find((s) => s.product.id === productId);
  }

  function getEffectiveStock(flower: any, colorId?: number): number {
    if (colorId && flower.color_stocks?.length > 0) {
      const cs = flower.color_stocks.find((c: any) => c.color.id === colorId);
      return cs ? cs.stock : 0;
    }
    return flower.stock;
  }

  function setQty(product: any, qty: number) {
    const sel = getSelection(product.id);
    const colorId = sel?.colorId;
    const effectiveStock = getEffectiveStock(product, colorId);
    if (qty < 0 || qty > effectiveStock) return;
    setSelection((prev) => {
      if (qty === 0) return prev.filter((s) => s.product.id !== product.id);
      const exists = prev.find((s) => s.product.id === product.id);
      if (exists) return prev.map((s) => s.product.id === product.id ? { ...s, quantity: qty } : s);
      return [...prev, { product, quantity: qty }];
    });
  }

  function setColor(product: any, colorId: number, colorName: string) {
    setSelection((prev) => {
      const exists = prev.find((s) => s.product.id === product.id);
      if (exists) {
        return prev.map((s) =>
          s.product.id === product.id
            ? { ...s, colorId, colorName, quantity: Math.min(s.quantity, getEffectiveStock(product, colorId)) }
            : s
        );
      }
      return [...prev, { product, quantity: 0, colorId, colorName }];
    });
    setColorError(null);
  }

  const activeItems = selection.filter((s) => s.quantity > 0);
  const isEmpty = activeItems.length === 0;
  const totalPrice = activeItems.reduce((sum, s) => sum + s.product.price * s.quantity, 0);

  function handleAddToCart() {
    if (isEmpty) return;

    const missingColor = activeItems.find(
      (s) => s.product.color_stocks?.length > 0 && !s.colorId
    );
    if (missingColor) {
      setColorError(`Please select a color for "${missingColor.product.name}"`);
      return;
    }

    const label = "Bouquet: " + activeItems.map((s) =>
      `${s.quantity}× ${s.product.name}${s.colorName ? ` (${s.colorName})` : ""}`
    ).join(", ");

    addBouquet({
      type: "bouquet",
      id: `bouquet-${Date.now()}`,
      label,
      flowers: activeItems.map((s) => ({
        product: s.product,
        quantity: s.quantity,
        colorId: s.colorId,
        colorName: s.colorName,
      })),
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
            const sel = getSelection(flower.id);
            const qty = sel?.quantity ?? 0;
            const hasColorVariants = flower.color_stocks?.length > 0;
            const effectiveStock = getEffectiveStock(flower, sel?.colorId);

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
                    <p className={styles.flowerMeta}>
                      {flower.price.toFixed(2)} RON / stem · {effectiveStock} available
                    </p>

                    {hasColorVariants ? (
                      <div className={styles.colorPickerRow}>
                        {flower.color_stocks.map((cs: any) => (
                          <button
                            key={cs.color.id}
                            className={`${styles.colorPickerBtn} ${sel?.colorId === cs.color.id ? styles.colorPickerBtnActive : ""} ${cs.stock === 0 ? styles.colorPickerBtnDisabled : ""}`}
                            onClick={() => cs.stock > 0 && setColor(flower, cs.color.id, cs.color.name)}
                            disabled={cs.stock === 0}
                            title={cs.stock === 0 ? `${cs.color.name} — out of stock` : cs.color.name}
                          >
                            <span className={styles.colorDot} style={{ background: cs.color.hex_code ?? "#ccc" }} />
                            <span>{cs.color.name}</span>
                            {cs.stock === 0 && <span className={styles.stockZero}>0</span>}
                          </button>
                        ))}
                      </div>
                    ) : (
                      flower.colors.length > 0 && (
                        <div className={styles.flowerColors}>
                          {flower.colors.map((c: any) => (
                            <span key={c.id} className={styles.colorDot} style={{ background: c.hex_code ?? "#ccc" }} title={c.name} />
                          ))}
                        </div>
                      )
                    )}
                  </div>
                </div>

                <div className={styles.qtyControl}>
                  {hasColorVariants && !sel?.colorId ? (
                    <span className={styles.selectColorHint}>Select color first</span>
                  ) : (
                    <>
                      <button className={styles.qtyBtn} onClick={() => setQty(flower, qty - 1)} disabled={qty === 0}>−</button>
                      <span className={styles.qtyValue}>{qty}</span>
                      <button className={styles.qtyBtn} onClick={() => setQty(flower, qty + 1)} disabled={qty >= effectiveStock}>+</button>
                    </>
                  )}
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
                <li key={`${s.product.id}-${s.colorId}`} className={styles.summaryRow}>
                  <span>
                    {s.quantity}× {s.product.name}
                    {s.colorName && (
                      <span className={styles.summaryColor}> ({s.colorName})</span>
                    )}
                  </span>
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
          {colorError && <p className={styles.colorError}>⚠️ {colorError}</p>}
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