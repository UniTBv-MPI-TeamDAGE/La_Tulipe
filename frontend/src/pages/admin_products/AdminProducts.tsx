import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  getProducts,
  getCategories,
  getColors,
  createProduct,
  updateProduct,
  deleteProduct,
  createCategory,
} from "../../services/productService";
import styles from "./AdminProducts.module.css";
import { useAuth } from "../../context/AuthContext";

const SEASONS = [
  { value: "all_season", label: "All season" },
  { value: "spring", label: "Spring" },
  { value: "summer", label: "Summer" },
  { value: "autumn", label: "Autumn" },
  { value: "winter", label: "Winter" },
];

const EMPTY_FORM = {
  name: "",
  description: "",
  price: 0,
  stock: 0,
  image_url: "",
  is_featured: false,
  season: "all_season",
  product_type: "individual",
  color_ids: [] as number[],
  category_id: 0,
};

export default function AdminProducts() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const isAdmin = user?.role === "admin";

  const [products, setProducts] = useState<any[]>([]);
  const [categories, setCategories] = useState<any[]>([]);
  const [colors, setColors] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [form, setForm] = useState({ ...EMPTY_FORM });
  const [submitting, setSubmitting] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);

  const [newCategoryName, setNewCategoryName] = useState("");
  const [addingCategory, setAddingCategory] = useState(false);

  useEffect(() => {
    if (!isAdmin) { navigate("/"); return; }
    loadAll();
  }, []);

  async function loadAll() {
    setLoading(true);
    try {
      const [p, c, col] = await Promise.all([getProducts(), getCategories(), getColors()]);
      setProducts(p);
      setCategories(c);
      setColors(col);
    } catch {
      //
    } finally {
      setLoading(false);
    }
  }

  function openCreate() {
    setEditingId(null);
    setForm({ ...EMPTY_FORM });
    setFormError(null);
    setShowForm(true);
  }

  function openEdit(product: any) {
    setEditingId(product.id);
    setForm({
      name: product.name,
      description: product.description,
      price: product.price,
      stock: product.stock,
      image_url: product.image_url ?? "",
      is_featured: product.is_featured,
      season: product.season,
      product_type: product.product_type,
      color_ids: product.colors.map((c: any) => c.id),
      category_id: product.category.id,
    });
    setFormError(null);
    setShowForm(true);
  }

  function closeForm() {
    setShowForm(false);
    setEditingId(null);
    setFormError(null);
  }

  async function handleSubmit() {
    if (!form.name.trim()) { setFormError("Name is required."); return; }
    if (form.price <= 0) { setFormError("Price must be greater than 0."); return; }
    if (form.category_id === 0) { setFormError("Please select a category."); return; }

    setSubmitting(true);
    setFormError(null);
    try {
      const payload = { ...form, image_url: form.image_url?.trim() || null };
      if (editingId !== null) {
        await updateProduct(editingId, payload);
      } else {
        await createProduct(payload);
      }
      closeForm();
      await loadAll();
    } catch (err: any) {
      setFormError(err.message ?? "Something went wrong.");
    } finally {
      setSubmitting(false);
    }
  }

  async function handleDelete(id: number, name: string) {
    if (!window.confirm(`Delete "${name}"?`)) return;
    try {
      await deleteProduct(id);
      await loadAll();
    } catch (err: any) {
      alert(err.message ?? "Failed to delete product.");
    }
  }

  async function handleAddCategory() {
    if (!newCategoryName.trim()) return;
    setAddingCategory(true);
    try {
      const cat = await createCategory(newCategoryName.trim());
      setCategories((prev) => [...prev, cat]);
      setNewCategoryName("");
    } catch (err: any) {
      alert(err.message ?? "Failed to create category.");
    } finally {
      setAddingCategory(false);
    }
  }

  function toggleColor(colorId: number) {
    setForm((prev) => ({
      ...prev,
      color_ids: prev.color_ids.includes(colorId)
        ? prev.color_ids.filter((id) => id !== colorId)
        : [...prev.color_ids, colorId],
    }));
  }

  if (!isAdmin) return null;

  return (
    <main className={styles.page}>
      <div className={styles.pageHeader}>
        <h1 className={styles.title}>Product Management</h1>
        <button className={styles.createBtn} onClick={openCreate}>+ Add product</button>
      </div>

      <div className={styles.categoryBar}>
        <span className={styles.categoryBarLabel}>Add category:</span>
        <input
          className={styles.categoryInput}
          type="text"
          placeholder="Category name"
          value={newCategoryName}
          onChange={(e) => setNewCategoryName(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleAddCategory()}
        />
        <button
          className={styles.categoryAddBtn}
          onClick={handleAddCategory}
          disabled={addingCategory || !newCategoryName.trim()}
        >
          {addingCategory ? "Adding…" : "Add"}
        </button>
        <div className={styles.categoryList}>
          {categories.map((c: any) => (
            <span key={c.id} className={styles.categoryChip}>{c.name}</span>
          ))}
        </div>
      </div>

      {loading ? (
        <div className={styles.stateBox}>
          <div className={styles.spinner} />
          <p>Loading…</p>
        </div>
      ) : (
        <div className={styles.tableWrapper}>
          <table className={styles.table}>
            <thead>
              <tr>
                <th>Image</th>
                <th>Name</th>
                <th>Category</th>
                <th>Type</th>
                <th>Price</th>
                <th>Stock</th>
                <th>Featured</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {products.map((p: any) => (
                <tr key={p.id}>
                  <td>
                    {p.image_url ? (
                      <img src={p.image_url} alt={p.name} className={styles.thumb} />
                    ) : (
                      <div className={styles.thumbFallback}>🌸</div>
                    )}
                  </td>
                  <td className={styles.tdName}>{p.name}</td>
                  <td>{p.category.name}</td>
                  <td>
                    <span className={p.product_type === "bouquet" ? styles.typeBouquet : styles.typeIndividual}>
                      {p.product_type}
                    </span>
                  </td>
                  <td>{p.price.toFixed(2)} RON</td>
                  <td>
                    <span className={p.stock === 0 ? styles.stockOut : styles.stockOk}>{p.stock}</span>
                  </td>
                  <td>{p.is_featured ? "✓" : "—"}</td>
                  <td className={styles.tdActions}>
                    <button className={styles.editBtn} onClick={() => openEdit(p)}>Edit</button>
                    <button className={styles.deleteBtn} onClick={() => handleDelete(p.id, p.name)}>Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {products.length === 0 && (
            <p className={styles.emptyTable}>No products yet. Click "Add product" to get started.</p>
          )}
        </div>
      )}

      {showForm && (
        <div className={styles.overlay} onClick={closeForm}>
          <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
            <div className={styles.modalHeader}>
              <h2>{editingId !== null ? "Edit product" : "Add product"}</h2>
              <button className={styles.closeBtn} onClick={closeForm}>✕</button>
            </div>

            <div className={styles.formGrid}>
              <div className={styles.field}>
                <label>Name *</label>
                <input className={styles.input} value={form.name}
                  onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
                  placeholder="e.g. Red Rose" />
              </div>

              <div className={styles.field}>
                <label>Category *</label>
                <select className={styles.input} value={form.category_id}
                  onChange={(e) => setForm((f) => ({ ...f, category_id: Number(e.target.value) }))}>
                  <option value={0}>Select category</option>
                  {categories.map((c: any) => (
                    <option key={c.id} value={c.id}>{c.name}</option>
                  ))}
                </select>
              </div>

              <div className={styles.field}>
                <label>Price (RON) *</label>
                <input className={styles.input} type="number" min={0} step={0.5} value={form.price}
                  onChange={(e) => setForm((f) => ({ ...f, price: Number(e.target.value) }))} />
              </div>

              <div className={styles.field}>
                <label>Stock</label>
                <input className={styles.input} type="number" min={0} value={form.stock}
                  onChange={(e) => setForm((f) => ({ ...f, stock: Number(e.target.value) }))} />
              </div>

              <div className={styles.field}>
                <label>Type</label>
                <select className={styles.input} value={form.product_type}
                  onChange={(e) => setForm((f) => ({ ...f, product_type: e.target.value }))}>
                  <option value="individual">Individual flower</option>
                  <option value="bouquet">Ready bouquet</option>
                </select>
              </div>

              <div className={styles.field}>
                <label>Season</label>
                <select className={styles.input} value={form.season}
                  onChange={(e) => setForm((f) => ({ ...f, season: e.target.value }))}>
                  {SEASONS.map((s) => (
                    <option key={s.value} value={s.value}>{s.label}</option>
                  ))}
                </select>
              </div>

              <div className={`${styles.field} ${styles.fieldFull}`}>
                <label>Image URL</label>
                <input className={styles.input} value={form.image_url}
                  onChange={(e) => setForm((f) => ({ ...f, image_url: e.target.value }))}
                  placeholder="https://…" />
              </div>

              <div className={`${styles.field} ${styles.fieldFull}`}>
                <label>Description</label>
                <textarea className={styles.textarea} value={form.description} rows={3}
                  onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))}
                  placeholder="Short description" />
              </div>

              <div className={`${styles.field} ${styles.fieldFull}`}>
                <label>Colors</label>
                <div className={styles.colorPicker}>
                  {colors.map((c: any) => (
                    <button key={c.id} type="button"
                      className={`${styles.colorOption} ${form.color_ids.includes(c.id) ? styles.colorSelected : ""}`}
                      onClick={() => toggleColor(c.id)} title={c.name}>
                      <span className={styles.colorSwatch} style={{ background: c.hex_code ?? "#ccc" }} />
                      {c.name}
                    </button>
                  ))}
                </div>
              </div>

              <div className={`${styles.field} ${styles.fieldFull}`}>
                <label className={styles.checkboxLabel}>
                  <input type="checkbox" checked={form.is_featured}
                    onChange={(e) => setForm((f) => ({ ...f, is_featured: e.target.checked }))} />
                  Mark as featured product
                </label>
              </div>
            </div>

            {formError && <p className={styles.formError}>⚠️ {formError}</p>}

            <div className={styles.modalFooter}>
              <button className={styles.cancelBtn} onClick={closeForm}>Cancel</button>
              <button className={styles.saveBtn} onClick={handleSubmit} disabled={submitting}>
                {submitting ? "Saving…" : editingId !== null ? "Save changes" : "Create product"}
              </button>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}