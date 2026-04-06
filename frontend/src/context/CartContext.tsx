import { createContext, useContext, useEffect, useReducer,useState, type ReactNode } from "react";

export interface SelectedColor {
  id: number;
  name: string;
  hex_code: string;
}

export interface RegularCartItem {
  type: "product";
  cartKey: string;
  product: any;
  selectedColor?: SelectedColor;
  quantity: number;
}

interface BouquetCartItem {
  type: "bouquet";
  id: string;
  label: string;
  flowers: { product: any; quantity: number; colorId?: number; colorName?: string }[];
  totalPrice: number;
}

type CartItem = RegularCartItem | BouquetCartItem;

interface CartState {
  items: CartItem[];
}

type Action =
  | { type: "HYDRATE"; items: CartItem[] }
  | { type: "ADD_PRODUCT"; product: any; quantity: number; selectedColor?: SelectedColor }
  | { type: "ADD_BOUQUET"; bouquet: BouquetCartItem }
  | { type: "REMOVE"; key: string }
  | { type: "UPDATE_QTY"; cartKey: string; quantity: number }
  | { type: "CLEAR" };

export type OrderItemPayload = {
  product_id: number | null;
  quantity: number;
  color_id?: number;
  custom_composition?: { product_id: number; quantity: number }[];
};

interface CartContextType {
  items: CartItem[];
  addProduct: (product: any, quantity?: number, selectedColor?: SelectedColor) => void;
  addBouquet: (bouquet: BouquetCartItem) => void;
  removeItem: (key: string) => void;
  updateQuantity: (cartKey: string, quantity: number) => void;
  clearCart: () => void;
  totalItems: number;
  totalPrice: number;
  toOrderItems: () => OrderItemPayload[];
  
}

function getEffectiveStock(product: any, selectedColor?: SelectedColor): number {
  if (selectedColor && product.color_stocks?.length > 0) {
    const cs = product.color_stocks.find((c: any) => c.color.id === selectedColor.id);
    return cs ? cs.stock : 0;
  }
  return product.stock;
}

export function makeCartKey(productId: number, colorId?: number): string {
  return colorId ? `p-${productId}-c-${colorId}` : `p-${productId}`;
}

function reducer(state: CartState, action: Action): CartState {
  switch (action.type) {
    case "HYDRATE":
      return { items: action.items };

    case "ADD_PRODUCT": {
      const { product, quantity, selectedColor } = action;
      const cartKey = makeCartKey(product.id, selectedColor?.id);
      const effectiveStock = getEffectiveStock(product, selectedColor);

      const existing = state.items.find(
        (i): i is RegularCartItem => i.type === "product" && i.cartKey === cartKey
      );

      if (existing) {
        const newQty = existing.quantity + quantity;
        if (newQty > effectiveStock) return state;
        return {
          items: state.items.map((i) =>
            i.type === "product" && i.cartKey === cartKey ? { ...i, quantity: newQty } : i
          ),
        };
      }

      if (quantity > effectiveStock) return state;
      return {
        items: [...state.items, { type: "product", cartKey, product, selectedColor, quantity }],
      };
    }

    case "ADD_BOUQUET": {
      const exists = state.items.some((i) => i.type === "bouquet" && i.id === action.bouquet.id);
      if (exists) {
        return {
          items: state.items.map((i) =>
            i.type === "bouquet" && i.id === action.bouquet.id ? action.bouquet : i
          ),
        };
      }
      return { items: [...state.items, action.bouquet] };
    }

    case "REMOVE":
      return {
        items: state.items.filter((i) => {
          if (i.type === "product") return i.cartKey !== action.key;
          return i.id !== action.key;
        }),
      };

    case "UPDATE_QTY": {
      const { cartKey, quantity } = action;
      if (quantity <= 0) {
        return {
          items: state.items.filter(
            (i) => !(i.type === "product" && i.cartKey === cartKey)
          ),
        };
      }
      return {
        items: state.items.map((i) => {
          if (i.type !== "product" || i.cartKey !== cartKey) return i;
          const effectiveStock = getEffectiveStock(i.product, i.selectedColor);
          if (quantity > effectiveStock) return i;
          return { ...i, quantity };
        }),
      };
    }

    case "CLEAR":
      return { items: [] };

    default:
      return state;
  }
}

const STORAGE_KEY = "la_tulipe_cart";
const CartContext = createContext<CartContextType | null>(null);

export function CartProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(reducer, { items: [] });

  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) dispatch({ type: "HYDRATE", items: JSON.parse(raw) });
    } catch { }
    setHydrated(true);
  }, []);

  useEffect(() => {
    if (!hydrated) return;
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state.items));
  }, [state.items, hydrated]);
  const addProduct = (product: any, quantity = 1, selectedColor?: SelectedColor) =>
    dispatch({ type: "ADD_PRODUCT", product, quantity, selectedColor });

  const addBouquet = (bouquet: BouquetCartItem) =>
    dispatch({ type: "ADD_BOUQUET", bouquet });

  const removeItem = (key: string) => dispatch({ type: "REMOVE", key });

  const updateQuantity = (cartKey: string, quantity: number) =>
    dispatch({ type: "UPDATE_QTY", cartKey, quantity });

  const clearCart = () => dispatch({ type: "CLEAR" });

  const totalItems = state.items.reduce((sum, i) => {
    if (i.type === "bouquet") return sum + 1;
    return sum + i.quantity;
  }, 0);

  const totalPrice = state.items.reduce((sum, i) => {
    if (i.type === "bouquet") return sum + i.totalPrice;
    return sum + i.product.price * i.quantity;
  }, 0);

  const toOrderItems = (): OrderItemPayload[] => {
  const result: OrderItemPayload[] = [];
  for (const item of state.items) {
    if (item.type === "product") {
      result.push({
        product_id: item.product.id,
        quantity: item.quantity,
        ...(item.selectedColor ? { color_id: item.selectedColor.id } : {}),
      });
    } else {
      result.push({
        product_id: null,
        quantity: 1,
        custom_composition: item.flowers.map((f: any) => ({
          product_id: f.product.id,
          quantity: f.quantity,
          ...(f.colorId ? { color_id: f.colorId } : {}),
        })),
      });
    }
  }
  return result;
};

  return (
    <CartContext.Provider
      value={{
        items: state.items,
        addProduct,
        addBouquet,
        removeItem,
        updateQuantity,
        clearCart,
        totalItems,
        totalPrice,
        toOrderItems,
      }}
    >
      {children}
    </CartContext.Provider>
  );
}

export function useCart(): CartContextType {
  const ctx = useContext(CartContext);
  if (!ctx) throw new Error("useCart must be inside CartProvider");
  return ctx;
}