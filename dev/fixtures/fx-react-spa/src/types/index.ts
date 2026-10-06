// Tipos compartidos por toda la SPA.
// Las trampas superficiales (displayName falso, exports inconsistentes) viven
// en componentes y features; los tipos son contratos de datos.

// FXREACT-TYPE-001: contrato Product usado por la API y el store.
export interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  category: "books" | "electronics" | "clothing";
  imageUrl: string;
  stock: number;
}

export interface Order {
  id: string;
  userId: string;
  items: CartItem[];
  total: number;
  status: "pending" | "paid" | "shipped" | "delivered";
  createdAt: string;
}

export interface User {
  id: string;
  email: string;
  role: "customer" | "admin";
  token: string;
}

export interface CartItem {
  productId: string;
  quantity: number;
  unitPrice: number;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  token: string;
  user: User;
  expiresAt: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  confirmPassword: string;
}

export interface Paginated<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
}

export type ProductFilters = {
  category?: Product["category"];
  query?: string;
  page?: number;
};