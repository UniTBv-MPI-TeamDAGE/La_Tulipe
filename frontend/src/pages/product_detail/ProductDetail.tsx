import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { getProductById } from "../../services/productService";
import { useCart } from "../../context/CartContext";
import styles from "./ProductDetail.module.css";

const SEASON_LABEL: Record<string, string> = {
  all_season: "All season",
  spring: "Spring",
  summer: "Summer",
  autumn: "Autumn",
  winter: "Winter",
};

export default function ProductDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { items, addProduct } = useCart();

  const [product, setProduct] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [notFound, setNotFound] = useState(false);
  const [quantity, setQuantity] = useState(1);
  const [justAdded, setJustAdded] = useState(false);

  useEffect(() => {
    if (!id) return;
    getProductById(Number(id))
      .then((p) => { setProduct(p); setQuantity(1); })
      .catch(() => setNotFound(true))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return <div className={styles.center}><div className={styles.spinner} /></div>;
  }

  if (notFound || !product) {
    return (
      <div className={styles.center}>
        <span className={styles.notFoundIcon}>🥀</span>
        <h2>Product not found</h2>
        <p>This product doesn't exist or has been removed.</p>
        <button className={styles.backBtn} onClick={() => navigate("/")}>Back to catalog</button>
      </div>
    );
  }

  const cartItem = items.find((i) => i.type === "product" && i.product.id === product.id);
  const inCart = cartItem?.type === "product" ? cartItem.quantity : 0;
  const remaining = product.stock - inCart;
  const outOfStock = product.stock === 0;

  function handleAdd() {
    if (quantity > remaining) return;
    addProduct(product, quantity);
    setJustAdded(true);
    setTimeout(() => setJustAdded(false), 1500);
  }

  return (
    <main className={styles.page}>
      <button className={styles.backLink} onClick={() => navigate(-1)}>
        ← Back to catalog
      </button>

      <div className={styles.layout}>
        <div className={styles.imageWrapper}>
          {product.image_url ? (
            <img src={product.image_url} alt={product.name} className={styles.image} />
          ) : (
            <div className={styles.imagePlaceholder}>🌸</div>
          )}
        </div>

        <div className={styles.details}>
          <p className={styles.categoryLabel}>{product.category.name}</p>
          <h1 className={styles.name}>{product.name}</h1>
          <p className={styles.price}>{product.price.toFixed(2)} RON</p>

          {product.description && <p className={styles.description}>{product.description}</p>}

          <div className={styles.metaGrid}>
            <span className={styles.metaKey}>Season</span>
            <span className={styles.metaVal}>{SEASON_LABEL[product.season]}</span>
            <span className={styles.metaKey}>Type</span>
            <span className={styles.metaVal}>
              {product.product_type === "bouquet" ? "Ready bouquet" : "Individual flower"}
            </span>
          </div>

          {product.colors.length > 0 && (
            <div className={styles.colorsRow}>
              <span className={styles.colorsLabel}>Colors:</span>
              {product.colors.map((c: any) => (
                <span
                  key={c.id}
                  className={styles.colorDot}
                  style={{ background: c.hex_code ?? "#ccc" }}
                  title={c.name}
                />
              ))}
            </div>
          )}

          <div className={styles.divider} />

          {outOfStock ? (
            <p className={styles.outOfStock}>⚠️ This product is currently unavailable.</p>
          ) : (
            <>
              <div className={styles.qtyRow}>
                <span className={styles.qtyLabel}>Quantity</span>
                <div className={styles.qtyControl}>
                  <button
                    className={styles.qtyBtn}
                    onClick={() => setQuantity((q) => Math.max(1, q - 1))}
                    disabled={quantity <= 1}
                  >−</button>
                  <span className={styles.qtyValue}>{quantity}</span>
                  <button
                    className={styles.qtyBtn}
                    onClick={() => setQuantity((q) => Math.min(remaining, q + 1))}
                    disabled={quantity >= remaining}
                  >+</button>
                </div>
                <span className={styles.stockNote}>
                  {product.stock} in stock{inCart > 0 && ` · ${inCart} in cart`}
                </span>
              </div>

              <button className={styles.addBtn} onClick={handleAdd} disabled={remaining <= 0}>
                {justAdded
                  ? "✓ Added to cart!"
                  : remaining <= 0
                  ? "Max stock reached"
                  : `Add ${quantity > 1 ? `${quantity} × ` : ""}to cart`}
              </button>
            </>
          )}
        </div>
      </div>
    </main>
  );
}