import { createContext, useContext, useEffect, useReducer,type ReactNode } from "react";

interface RegularCartItem {
  type: "product";
  product: any;
  quantity: number;
}

interface BouquetCartItem {
  type: "bouquet";
  id: string;
  label: string;
  flowers: { product: any; quantity: number }[];
  totalPrice: number;
}

type CartItem = RegularCartItem | BouquetCartItem;

interface CartState {
  items: CartItem[];
}

type Action =
  | { type: "HYDRATE"; items: CartItem[] }
  | { type: "ADD_PRODUCT"; product: any; quantity: number }
  | { type: "ADD_BOUQUET"; bouquet: BouquetCartItem }
  | { type: "REMOVE"; id: number | string }
  | { type: "UPDATE_QTY"; productId: number; quantity: number }
  | { type: "CLEAR" };

interface CartContextType {
  items: CartItem[];
  addProduct: (product: any, quantity?: number) => void;
  addBouquet: (bouquet: BouquetCartItem) => void;
  removeItem: (id: number | string) => void;
  updateQuantity: (productId: number, quantity: number) => void;
  clearCart: () => void;
  totalItems: number;
  totalPrice: number;
  toOrderItems: () => { product_id: number; quantity: number }[];
}

function reducer(state: CartState, action: Action): CartState {
  switch (action.type) {
    case "HYDRATE":
      return { items: action.items };

    case "ADD_PRODUCT": {
      const { product, quantity } = action;
      const existing = state.items.find(
        (i): i is RegularCartItem =>
          i.type === "product" && i.product.id === product.id
      );
      if (existing) {
        const newQty = existing.quantity + quantity;
        if (newQty > product.stock) return state;
        return {
          items: state.items.map((i) =>
            i.type === "product" && i.product.id === product.id
              ? { ...i, quantity: newQty }
              : i
          ),
        };
      }
      if (quantity > product.stock) return state;
      return {
        items: [...state.items, { type: "product", product, quantity }],
      };
    }

    case "ADD_BOUQUET": {
      const exists = state.items.some(
        (i) => i.type === "bouquet" && i.id === action.bouquet.id
      );
      if (exists) {
        return {
          items: state.items.map((i) =>
            i.type === "bouquet" && i.id === action.bouquet.id
              ? action.bouquet
              : i
          ),
        };
      }
      return { items: [...state.items, action.bouquet] };
    }

    case "REMOVE":
      return {
        items: state.items.filter((i) => {
          if (i.type === "product") return i.product.id !== action.id;
          return i.id !== action.id;
        }),
      };

    case "UPDATE_QTY": {
      const { productId, quantity } = action;
      if (quantity <= 0) {
        return {
          items: state.items.filter(
            (i) => !(i.type === "product" && i.product.id === productId)
          ),
        };
      }
      return {
        items: state.items.map((i) => {
          if (i.type !== "product" || i.product.id !== productId) return i;
          if (quantity > i.product.stock) return i;
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

  useEffect(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) dispatch({ type: "HYDRATE", items: JSON.parse(raw) });
    } catch {
      //
    }
  }, []);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state.items));
  }, [state.items]);

  const addProduct = (product: any, quantity = 1) =>
    dispatch({ type: "ADD_PRODUCT", product, quantity });

  const addBouquet = (bouquet: BouquetCartItem) =>
    dispatch({ type: "ADD_BOUQUET", bouquet });

  const removeItem = (id: number | string) =>
    dispatch({ type: "REMOVE", id });

  const updateQuantity = (productId: number, quantity: number) =>
    dispatch({ type: "UPDATE_QTY", productId, quantity });

  const clearCart = () => dispatch({ type: "CLEAR" });

  const totalItems = state.items.reduce((sum, i) => {
    if (i.type === "bouquet") return sum + 1;
    return sum + i.quantity;
  }, 0);

  const totalPrice = state.items.reduce((sum, i) => {
    if (i.type === "bouquet") return sum + i.totalPrice;
    return sum + i.product.price * i.quantity;
  }, 0);

  const toOrderItems = () => {
    const result: { product_id: number; quantity: number }[] = [];
    for (const item of state.items) {
      if (item.type === "product") {
        result.push({ product_id: item.product.id, quantity: item.quantity });
      } else {
        for (const f of item.flowers) {
          result.push({ product_id: f.product.id, quantity: f.quantity });
        }
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