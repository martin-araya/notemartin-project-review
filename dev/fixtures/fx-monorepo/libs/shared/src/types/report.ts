import type { ListingFilters } from './listing.js';

export type ReportFormat = 'csv' | 'json';

export interface ExportRequest {
  filters: ListingFilters;
  format: ReportFormat;
}

export interface ExportResponse {
  url: string;
  format: ReportFormat;
  rows: number;
  expiresAt: string;
}
