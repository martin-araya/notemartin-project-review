// RTK Query: define los endpoints de la API.
// Trampa del ecosistema #2: los hooks como useGetProductsQuery NO estan
// definidos literalmente aqui; createApi los genera a partir de los builders
// `query` y `mutation`. La skill debe leer los endpoints y notar la generacion
// implicita.

import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { API_BASE_URL, TOKEN_HEADER, TOKEN_PREFIX } from "../lib/env.js";
import type {
  Product,
  Order,
  User,
  LoginRequest,
  LoginResponse,
  RegisterRequest,
  Paginated,
  ProductFilters,
} from "../types/index.js";

export interface ProductsArgs extends Partial<ProductFilters> {
  pageSize?: number;
}

export const baseApi = createApi({
  reducerPath: "api",
  baseQuery: fetchBaseQuery({
    baseUrl: API_BASE_URL,
    prepareHeaders: (headers, { getState }) => {
      const token = (getState() as { auth?: { token?: string } }).auth?.token;
      if (token) {
        headers.set(TOKEN_HEADER, `${TOKEN_PREFIX}${token}`);
      }
      return headers;
    },
  }),
  tagTypes: ["Product", "Order", "User"],
  endpoints: (builder) => ({
    // FXREACT-API-001: endpoint autogenera useLoginMutation.
    login: builder.mutation<LoginResponse, LoginRequest>({
      query: (credentials) => ({
        url: "/auth/login",
        method: "POST",
        body: credentials,
      }),
    }),
    // FXREACT-API-002: endpoint autogenera useRegisterMutation.
    register: builder.mutation<User, RegisterRequest>({
      query: (body) => ({
        url: "/auth/register",
        method: "POST",
        body,
      }),
    }),
    // FXREACT-API-003: endpoint autogenera useGetProductsQuery.
    getProducts: builder.query<Paginated<Product>, ProductsArgs>({
      query: (args) => {
        const params = new URLSearchParams();
        if (args?.category) params.set("category", args.category);
        if (args?.query) params.set("q", args.query);
        if (args?.page) params.set("page", String(args.page));
        if (args?.pageSize) params.set("pageSize", String(args.pageSize));
        return { url: `/products?${params.toString()}` };
      },
      providesTags: (result) =>
        result
          ? [
              ...result.items.map((p) => ({ type: "Product" as const, id: p.id })),
              { type: "Product", id: "LIST" },
            ]
          : [{ type: "Product", id: "LIST" }],
    }),
    // FXREACT-API-004: endpoint autogenera useGetProductQuery.
    getProduct: builder.query<Product, string>({
      query: (id) => `/products/${id}`,
      providesTags: (_r, _e, id) => [{ type: "Product", id }],
    }),
    // FXREACT-API-005: endpoint autogenera useGetOrdersQuery.
    getOrders: builder.query<Paginated<Order>, { status?: Order["status"]; page?: number }>({
      query: (args) => {
        const params = new URLSearchParams();
        if (args?.status) params.set("status", args.status);
        if (args?.page) params.set("page", String(args.page));
        return { url: `/orders?${params.toString()}` };
      },
      providesTags: (result) =>
        result
          ? [
              ...result.items.map((o) => ({ type: "Order" as const, id: o.id })),
              { type: "Order", id: "LIST" },
            ]
          : [{ type: "Order", id: "LIST" }],
    }),
  }),
});

// FXREACT-API-EXPORT: los hooks se generan a partir de los endpoints arriba.
// NO hay `function useGetProductsQuery(...)` literal en el codigo fuente.
export const {
  useLoginMutation,
  useRegisterMutation,
  useGetProductsQuery,
  useGetProductQuery,
  useGetOrdersQuery,
} = baseApi.endpoints;