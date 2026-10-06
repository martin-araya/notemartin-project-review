// Module file
export interface Aprobacion {
  id: string;
  itemId: string;
  usuarioId: string;
  decision: 'aprobado' | 'rechazado';
  comentario?: string;
  fecha: string;
}

export interface AprobacionesState {
  items: Aprobacion[];
  loading: boolean;
}

export const APROBACIONES_FEATURE_KEY = 'aprobaciones';
