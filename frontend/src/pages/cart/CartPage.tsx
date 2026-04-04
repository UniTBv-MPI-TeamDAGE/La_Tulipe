import { useNavigate } from "react-router-dom";
import { useCart, type RegularCartItem } from "../../context/CartContext";
import styles from "./CartPage.module.css";

export default function CartPage() {
  const navigate = useNavigate();
  const { items, removeItem, updateQuantity, totalPrice } = useCart();

  if (items.length === 0) {
    return (
      <main className={styles.page}>
        <div className={styles.empty}>
          <span className={styles.emptyIcon}>🛒</span>
          <h2>Your cart is empty</h2>
          <p>Discover our flowers and add your favorites.</p>
          <button className={styles.catalogBtn} onClick={() => navigate("/")}>
            Go to catalog
          </button>
        </div>
      </main>
    );
  }

  return (
    <main className={styles.page}>
      <h1 className={styles.title}>Your cart</h1>

      <div className={styles.layout}>
        <div className={styles.itemList}>
          {items.map((item) => {
            if (item.type === "bouquet") {
              return (
                <div key={item.id} className={styles.card}>
                  <div className={styles.cardImage}>
                    <div className={styles.imageFallback}>🌺</div>
                  </div>
                  <div className={styles.cardBody}>
                    <p className={styles.cardName}>{item.label}</p>
                    <p className={styles.cardMeta}>Custom bouquet</p>
                  </div>
                  <div className={styles.cardRight}>
                    <p className={styles.cardPrice}>{item.totalPrice.toFixed(2)} RON</p>
                    <button
                      className={styles.removeBtn}
                      onClick={() => removeItem(item.id)}
                    >
                      Remove
                    </button>
                  </div>
                </div>
              );
            }

            const reg = item as RegularCartItem;
            const subtotal = reg.product.price * reg.quantity;
            const effectiveStock = reg.selectedColor
              ? (reg.product.color_stocks?.find((cs: any) => cs.color.id === reg.selectedColor!.id)?.stock ?? reg.product.stock)
              : reg.product.stock;

            return (
              <div key={reg.cartKey} className={styles.card}>
                <div className={styles.cardImage}>
                  {reg.product.image_url ? (
                    <img src={reg.product.image_url} alt={reg.product.name} className={styles.image} />
                  ) : (
                    <div className={styles.imageFallback}>🌸</div>
                  )}
                </div>
                <div className={styles.cardBody}>
                  <p className={styles.cardName}>
                    {reg.product.name}
                    {reg.selectedColor && (
                      <span className={styles.colorTag}>
                        <span
                          className={styles.colorDot}
                          style={{ background: reg.selectedColor.hex_code }}
                        />
                        {reg.selectedColor.name}
                      </span>
                    )}
                  </p>
                  <p className={styles.cardMeta}>{reg.product.price.toFixed(2)} RON / item</p>
                  <div className={styles.qtyControl}>
                    <button
                      className={styles.qtyBtn}
                      onClick={() => updateQuantity(reg.cartKey, reg.quantity - 1)}
                      disabled={reg.quantity <= 1}
                    >−</button>
                    <span className={styles.qtyValue}>{reg.quantity}</span>
                    <button
                      className={styles.qtyBtn}
                      onClick={() => updateQuantity(reg.cartKey, reg.quantity + 1)}
                      disabled={reg.quantity >= effectiveStock}
                    >+</button>
                  </div>
                </div>
                <div className={styles.cardRight}>
                  <p className={styles.cardPrice}>{subtotal.toFixed(2)} RON</p>
                  <button
                    className={styles.removeBtn}
                    onClick={() => removeItem(reg.cartKey)}
                  >
                    Remove
                  </button>
                </div>
              </div>
            );
          })}
        </div>

        <aside className={styles.summary}>
          <h2 className={styles.summaryTitle}>Summary</h2>
          <div className={styles.summaryRow}>
            <span>Subtotal</span>
            <strong>{totalPrice.toFixed(2)} RON</strong>
          </div>
          <div className={styles.summaryRow}>
            <span>Delivery</span>
            <span className={styles.free}>Free</span>
          </div>
          <div className={`${styles.summaryRow} ${styles.summaryTotal}`}>
            <span>Total</span>
            <strong>{totalPrice.toFixed(2)} RON</strong>
          </div>
          <button
            className={styles.checkoutBtn}
            onClick={() => navigate("/checkout")}
          >
            Place order →
          </button>
          <button
            className={styles.continueBtn}
            onClick={() => navigate("/")}
          >
            Continue shopping
          </button>
        </aside>
      </div>
    </main>
  );
}