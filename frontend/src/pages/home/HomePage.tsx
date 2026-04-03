import { useCallback, useEffect, useRef, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { getProducts, getFeaturedProducts, getCategories } from "../../services/productService";
import ProductCard from "../../components/shared/product_card/ProductCard";
import styles from "./HomePage.module.css";

export default function HomePage() {
  const [searchParams, setSearchParams] = useSearchParams();

  const urlSearch = searchParams.get("search") ?? "";
  const [selectedCategory, setSelectedCategory] = useState(searchParams.get("category") ?? "");
  const [minPrice, setMinPrice] = useState(searchParams.get("min_price") ?? "");
  const [maxPrice, setMaxPrice] = useState(searchParams.get("max_price") ?? "");

  const [products, setProducts] = useState<any[]>([]);
  const [featured, setFeatured] = useState<any[]>([]);
  const [categories, setCategories] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    getCategories().then(setCategories).catch(() => {});
    getFeaturedProducts().then(setFeatured).catch(() => {});
  }, []);

  const fetchProducts = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getProducts({
        search: urlSearch,
        category: selectedCategory,
        min_price: minPrice,
        max_price: maxPrice,
      });
      setProducts(data);
    } catch (err: any) {
      setError(err.message ?? "Failed to load products.");
    } finally {
      setLoading(false);
    }
  }, [urlSearch, selectedCategory, minPrice, maxPrice]);

  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(fetchProducts, 150);
    return () => { if (debounceRef.current) clearTimeout(debounceRef.current); };
  }, [fetchProducts]);

  const hasFilters = urlSearch.length >= 2 || selectedCategory || minPrice || maxPrice;

  function resetFilters() {
    setSelectedCategory("");
    setMinPrice("");
    setMaxPrice("");
    setSearchParams({});
  }

  function handleCategoryChange(val: string) {
    setSelectedCategory(val);
    const next = new URLSearchParams(searchParams);
    if (val) next.set("category", val);
    else next.delete("category");
    setSearchParams(next);
  }

  return (
    <main className={styles.page}>
      {!hasFilters && (
        <section className={styles.hero}>
          <h1 className={styles.heroTitle}>La Tulipe</h1>
          <p className={styles.heroSub}>Fresh flowers, delivered with care</p>
        </section>
      )}

      <section className={styles.filterBar}>
        <select
          className={styles.select}
          value={selectedCategory}
          onChange={(e) => handleCategoryChange(e.target.value)}
        >
          <option value="">All categories</option>
          {categories.map((c: any) => (
            <option key={c.id} value={c.name}>{c.name}</option>
          ))}
        </select>

        <div className={styles.priceRange}>
          <input
            className={styles.priceInput}
            type="number"
            placeholder="Min price"
            value={minPrice}
            min={0}
            onChange={(e) => setMinPrice(e.target.value)}
          />
          <span className={styles.priceSep}>–</span>
          <input
            className={styles.priceInput}
            type="number"
            placeholder="Max price"
            value={maxPrice}
            min={0}
            onChange={(e) => setMaxPrice(e.target.value)}
          />
        </div>

        {hasFilters && (
          <button className={styles.resetBtn} onClick={resetFilters}>
            Clear filters
          </button>
        )}
      </section>

      {!hasFilters && featured.length > 0 && (
        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>✦ Featured</h2>
          <div className={styles.grid}>
            {featured.map((p: any) => <ProductCard key={p.id} product={p} />)}
          </div>
        </section>
      )}

      <section className={styles.section}>
        <h2 className={styles.sectionTitle}>
          {hasFilters ? (
            <>
              🔍 Results
              {!loading && (
                <span className={styles.count}>
                  {products.length} product{products.length !== 1 ? "s" : ""}
                </span>
              )}
            </>
          ) : "✦ All flowers"}
        </h2>

        {loading && (
          <div className={styles.stateBox}>
            <div className={styles.spinner} />
            <p>Loading products…</p>
          </div>
        )}
        {!loading && error && (
          <div className={styles.stateBox}>
            <p className={styles.errorText}>⚠️ {error}</p>
            <button className={styles.retryBtn} onClick={fetchProducts}>Try again</button>
          </div>
        )}
        {!loading && !error && products.length === 0 && (
          <div className={styles.stateBox}>
            <p>No products found for your search.</p>
            {hasFilters && (
              <button className={styles.resetBtn} onClick={resetFilters}>Clear filters</button>
            )}
          </div>
        )}
        {!loading && !error && products.length > 0 && (
          <div className={styles.grid}>
            {products.map((p: any) => <ProductCard key={p.id} product={p} />)}
          </div>
        )}
      </section>
    </main>
  );
}