export type ListingStatus = 'draft' | 'active' | 'sold' | 'archived';

export interface Listing {
  id: string;
  title: string;
  description: string;
  price: number;
  currency: string;
  status: ListingStatus;
  ownerId: string;
  createdAt: string;
  updatedAt: string;
}

export interface ListingFilters {
  status?: ListingStatus;
  minPrice?: number;
  maxPrice?: number;
  query?: string;
  ownerId?: string;
  page?: number;
  pageSize?: number;
}

export interface PaginatedListings {
  items: Listing[];
  total: number;
  page: number;
  pageSize: number;
}
