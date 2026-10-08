/**
 * Trampa E1 + E2: lista tipada de channels IPC para que el codigo
 * TypeScript no rompa, pero el contrato sigue siendo por string en runtime.
 */
import { IPC_CHANNELS, type IpcChannel } from './handlers';

/**
 * Superficie expuesta via `contextBridge.exposeInMainWorld('api', ...)`.
 * La skill debe notar que esta es la superficie que el renderer usa.
 */
export interface ExposedApi {
  openProjectDialog: () => Promise<string | null>;
  openProject: (args: { path: string }) => Promise<{
    path: string;
    content: string;
    size: number;
    modified: number;
    name: string;
  }>;
  exportPdf: (args: { content: string; format?: 'a4' | 'letter' }) => Promise<{ path: string; size: number } | null>;
  checkUpdate: () => Promise<{ available: boolean; version?: string }>;
  installUpdate: () => Promise<boolean>;
  onMenuDispatch: (callback: (action: string) => void) => void;
}

export const CHANNEL_LIST: IpcChannel[] = Object.values(IPC_CHANNELS);