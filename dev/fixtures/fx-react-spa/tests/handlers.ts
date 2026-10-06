// MSW v2 handlers: backend en memoria para RTK Query y los loaders/actions.
// Reset entre tests para que las mutaciones no se acumulen.

import { http, HttpResponse } from "msw";
import { setupServer } from "msw/node";
import type { Product, Order, User, LoginResponse, Paginated } from "../src/types/index.js";

const products: Product[] = [
  {
    id: "p1",
    name: "El Quijote",
    description: "Clasico de la literatura",
    price: 19.95,
    category: "books",
    imageUrl: "/img/quijote.png",
    stock: 12,
  },
  {
    id: "p2",
    name: "Audifonos BT",
    description: "Inalambricos con estuche",
    price: 49.0,
    category: "electronics",
    imageUrl: "/img/bt.png",
    stock: 5,
  },
  {
    id: "p3",
    name: "Camiseta",
    description: "Algodon organico",
    price: 14.5,
    category: "clothing",
    imageUrl: "/img/shirt.png",
    stock: 30,
  },
];

const orders: Order[] = [];

const users: Array<User & { password: string }> = [
  {
    id: "u1",
    email: "user@example.com",
    role: "customer",
    token: "test-token",
    password: "password123",
  },
];

function paginate<T>(items: T[], page = 1, pageSize = 20): Paginated<T> {
  return { items, total: items.length, page, pageSize };
}

export const handlers = [
  http.post("/api/auth/login", async ({ request }) => {
    const body = (await request.json()) as { email: string; password: string };
    const user = users.find((u) => u.email === body.email && u.password === body.password);
    if (!user) {
      return HttpResponse.json({ message: "invalid_credentials" }, { status: 401 });
    }
    const res: LoginResponse = {
      token: user.token,
      user: { id: user.id, email: user.email, role: user.role, token: user.token },
      expiresAt: new Date(Date.now() + 3600_000).toISOString(),
    };
    return HttpResponse.json(res);
  }),

  http.post("/api/auth/register", async ({ request }) => {
    const body = (await request.json()) as { email: string; password: string };
    if (users.find((u) => u.email === body.email)) {
      return HttpResponse.json({ message: "email_exists" }, { status: 409 });
    }
    const newUser: User = {
      id: `u${users.length + 1}`,
      email: body.email,
      role: "customer",
      token: `tok-${Date.now()}`,
    };
    users.push({ ...newUser, password: body.password });
    return HttpResponse.json(newUser);
  }),

  http.get("/api/products", ({ request }) => {
    const url = new URL(request.url);
    const q = url.searchParams.get("q");
    const cat = url.searchParams.get("category");
    let filtered = products;
    if (q) filtered = filtered.filter((p) => p.name.toLowerCase().includes(q.toLowerCase()));
    if (cat) filtered = filtered.filter((p) => p.category === cat);
    return HttpResponse.json(paginate(filtered));
  }),

  http.get("/api/products/:id", ({ params }) => {
    const p = products.find((x) => x.id === params.id);
    if (!p) return HttpResponse.json({ message: "not_found" }, { status: 404 });
    return HttpResponse.json(p);
  }),

  http.get("/api/orders", ({ request }) => {
    const url = new URL(request.url);
    const status = url.searchParams.get("status");
    let filtered = orders;
    if (status) filtered = filtered.filter((o) => o.status === status);
    return HttpResponse.json(paginate(filtered));
  }),

  http.post("/api/orders", async ({ request }) => {
    const body = (await request.json()) as { items: Order["items"] };
    const total = body.items.reduce((acc, i) => acc + i.unitPrice * i.quantity, 0);
    const order: Order = {
      id: `o${orders.length + 1}`,
      userId: "u1",
      items: body.items,
      total,
      status: "paid",
      createdAt: new Date().toISOString(),
    };
    orders.push(order);
    return HttpResponse.json(order, { status: 201 });
  }),
];

export const server = setupServer(...handlers);