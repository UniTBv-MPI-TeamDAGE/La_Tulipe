const BASE = import.meta.env.VITE_API_URL ?? "";

function authHeader(): Record<string, string> {
  const token = localStorage.getItem("access_token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function getProducts(filters: {
  search?: string;
  category?: string;
  type?: string;
  min_price?: string;
  max_price?: string;
  color_id?: string | number;
} = {}) {
  const params = new URLSearchParams();
  if (filters.search && filters.search.length >= 2) params.set("search", filters.search);
  if (filters.category) params.set("category", filters.category);
  if (filters.type) params.set("type", filters.type);
  if (filters.min_price) params.set("min_price", filters.min_price);
  if (filters.max_price) params.set("max_price", filters.max_price);
  if (filters.color_id) params.set("color", String(filters.color_id));
  const qs = params.toString();
  const res = await fetch(`${BASE}/api/products${qs ? `?${qs}` : ""}`);
  if (!res.ok) throw new Error("Failed to load products");
  return res.json();
}

export async function getFeaturedProducts() {
  const res = await fetch(`${BASE}/api/products/featured`);
  if (!res.ok) throw new Error("Failed to load featured products");
  return res.json();
}

export async function getProductById(id: number) {
  const res = await fetch(`${BASE}/api/products/${id}`);
  if (res.status === 404) {
    const err = new Error("Product not found");
    (err as any).status = 404;
    throw err;
  }
  if (!res.ok) throw new Error("Failed to load product");
  return res.json();
}

export async function getCategories() {
  const res = await fetch(`${BASE}/api/categories`);
  if (!res.ok) throw new Error("Failed to load categories");
  return res.json();
}

export async function getColors() {
  const res = await fetch(`${BASE}/api/colors`, { headers: authHeader() });
  if (!res.ok) throw new Error("Failed to load colors");
  return res.json();
}

export async function createProduct(data: {
  name: string;
  description: string;
  price: number;
  stock: number;
  image_url?: string | null;
  is_featured: boolean;
  season: string;
  product_type: string;
  color_stocks: { color_id: number; stock: number }[];
  category_id: number;
}) {
  const res = await fetch(`${BASE}/api/products`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeader() },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail ?? "Failed to create product");
  }
  return res.json();
}

export async function updateProduct(id: number, data: {
  name?: string;
  description?: string;
  price?: number;
  stock?: number;
  image_url?: string | null;
  is_featured?: boolean;
  season?: string;
  product_type?: string;
  color_stocks?: { color_id: number; stock: number }[];
  category_id?: number;
}) {
  const res = await fetch(`${BASE}/api/products/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json", ...authHeader() },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail ?? "Failed to update product");
  }
  return res.json();
}

export async function deleteProduct(id: number) {
  const res = await fetch(`${BASE}/api/products/${id}`, {
    method: "DELETE",
    headers: authHeader(),
  });
  if (!res.ok) throw new Error("Failed to delete product");
}

export async function createCategory(name: string) {
  const res = await fetch(`${BASE}/api/categories`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeader() },
    body: JSON.stringify({ name }),
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail ?? "Failed to create category");
  }
  return res.json();
}