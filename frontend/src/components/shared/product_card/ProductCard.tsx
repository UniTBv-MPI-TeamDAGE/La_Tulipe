import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useCart, makeCartKey } from "../../../context/CartContext";
import styles from "./ProductCard.module.css";

interface Props {
  product: any;
}

export default function ProductCard({ product }: Props) {
  const navigate = useNavigate();
  const { items, addProduct } = useCart();
  const [justAdded, setJustAdded] = useState(false);

  const hasColorVariants = product.color_stocks?.length > 0;

  const cartKey = makeCartKey(product.id);
  const cartItem = items.find((i) => i.type === "product" && i.cartKey === cartKey);
  const cartQty = cartItem?.type === "product" ? cartItem.quantity : 0;
  const outOfStock = product.stock === 0;
  const atMax = !hasColorVariants && cartQty >= product.stock;

  function handleAdd(e: React.MouseEvent) {
    e.stopPropagation();
    if (hasColorVariants) {
      navigate(`/products/${product.id}`);
      return;
    }
    if (outOfStock || atMax) return;
    addProduct(product, 1);
    setJustAdded(true);
    setTimeout(() => setJustAdded(false), 1400);
  }

  return (
    <article
      className={styles.card}
      onClick={() => navigate(`/products/${product.id}`)}
    >
      <div className={styles.imageWrapper}>
        {product.image_url ? (
          <img
            src={product.image_url}
            alt={product.name}
            className={styles.image}
            loading="lazy"
          />
        ) : (
          <div className={styles.placeholder}>🌸</div>
        )}
        {outOfStock && <span className={styles.badgeOut}>Out of stock</span>}
        {product.is_featured && !outOfStock && (
          <span className={styles.badgeFeatured}>Featured</span>
        )}
      </div>
      <div className={styles.body}>
        <p className={styles.categoryLabel}>{product.category.name}</p>
        <h3 className={styles.name}>{product.name}</h3>
        <div className={styles.priceRow}>
          <span className={styles.price}>{product.price.toFixed(2)} RON</span>
          {!outOfStock && <span className={styles.stock}>{product.stock} left</span>}
        </div>
        <button
          className={`${styles.addBtn} ${justAdded ? styles.addBtnDone : ""}`}
          onClick={handleAdd}
          disabled={!hasColorVariants && (outOfStock || atMax)}
        >
          {hasColorVariants
            ? "Choose color →"
            : justAdded
            ? "✓ Added!"
            : atMax
            ? "Max reached"
            : "Add to cart"}
        </button>
      </div>
    </article>
  );
}