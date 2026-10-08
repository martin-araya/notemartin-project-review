/**
 * Trampa E2: contextBridge expone `window.api` con la lista tipada de funciones.
 * Trampa P4: las funciones NO envuelven `Function` (no serializable); el
 * bridge solo expone strings, numbers, arrays y objetos planos.
 */
import { contextBridge, ipcRenderer } from 'electron';

import { IPC_CHANNELS } from '../main/ipc/handlers';

const api = {
  openProjectDialog: () =>
    ipcRenderer.invoke(IPC_CHANNELS.PROJECT_OPEN_DIALOG),

  openProject: (args: { path: string }) =>
    ipcRenderer.invoke(IPC_CHANNELS.PROJECT_OPEN, args),

  exportPdf: (args: { content: string; format?: 'a4' | 'letter' }) =>
    ipcRenderer.invoke(IPC_CHANNELS.PDF_EXPORT, args),

  checkUpdate: () =>
    ipcRenderer.invoke(IPC_CHANNELS.UPDATE_CHECK),

  installUpdate: () =>
    ipcRenderer.invoke(IPC_CHANNELS.UPDATE_INSTALL),

  onMenuDispatch: (callback: (action: string) => void) => {
    ipcRenderer.on(IPC_CHANNELS.MENU_DISPATCH, (_event, action: string) => {
      callback(action);
    });
  },
};

contextBridge.exposeInMainWorld('api', api);

export type FxElectronApi = typeof api;