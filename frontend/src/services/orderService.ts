const BASE = import.meta.env.VITE_API_URL ?? "";

function authHeader(): Record<string, string> {
  const token = localStorage.getItem("access_token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function createOrder(data: {
  customer_name: string;
  customer_email: string;
  customer_phone: string;
  delivery_address: string;
  card_message?: string | null;
  items: { product_id: number; quantity: number }[];
}) {
  const res = await fetch(`${BASE}/api/orders`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeader() },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    const err = new Error(body.detail ?? "Failed to place order");
    (err as any).status = res.status;
    throw err;
  }
  return res.json();
}

export async function getMyOrders() {
  const res = await fetch(`${BASE}/api/orders/my-orders`, {
    headers: authHeader(),
  });
  if (res.status === 401) {
    const err = new Error("Unauthorized");
    (err as any).status = 401;
    throw err;
  }
  if (!res.ok) throw new Error("Failed to load orders");
  return res.json();
}

export async function getMyOrderById(id: number) {
  const res = await fetch(`${BASE}/api/orders/${id}`, {
    headers: authHeader(),
  });
  if (res.status === 404) {
    const err = new Error("Order not found");
    (err as any).status = 404;
    throw err;
  }
  if (!res.ok) throw new Error("Failed to load order");
  return res.json();
}