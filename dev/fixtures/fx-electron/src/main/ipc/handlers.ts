/**
 * Trampa E1: contratos IPC declarados como strings sin tipado fuerte.
 * El contrato es solo por convencion entre main y renderer.
 * Trampa P1: handlers sin try/catch que lanzan excepciones no controladas.
 */
import { ipcMain, dialog, BrowserWindow, shell, app } from 'electron';
import { promises as fs } from 'fs';
import path from 'path';

import { exportPdfForWindow } from '../workers/pdfExporter';
import { spawnUpdater } from '../workers/updater';

/**
 * IPC channel names como strings (trampa E1 + trampa E2).
 * La skill debe seguir estos strings desde main hasta preload/api.ts.
 */
export const IPC_CHANNELS = {
  PROJECT_OPEN: 'project:open',
  PROJECT_OPEN_DIALOG: 'project:open-dialog',
  PDF_EXPORT: 'pdf:export',
  PDF_EXPORT_DIALOG: 'pdf:export-dialog',
  UPDATE_CHECK: 'update:check',
  UPDATE_INSTALL: 'update:install',
  MENU_DISPATCH: 'menu:dispatch',
} as const;

export type IpcChannel = (typeof IPC_CHANNELS)[keyof typeof IPC_CHANNELS];

interface OpenProjectArgs {
  path?: string;
}

interface ExportPdfArgs {
  content: string;
  format?: 'a4' | 'letter';
}

/**
 * Trampa P1: handlers sin try/catch.
 * Si openProject falla (archivo corrupto, permisos), la promesa
 * rechazada se propaga al renderer sin manejo explicito.
 */
export function registerIpcHandlers(getWindow: () => BrowserWindow | null): void {
  ipcMain.handle(IPC_CHANNELS.PROJECT_OPEN_DIALOG, async () => {
    const win = getWindow();
    const result = await dialog.showOpenDialog(win!, {
      properties: ['openFile'],
      filters: [
        { name: 'Documents', extensions: ['txt', 'md', 'json', 'xml'] },
        { name: 'All Files', extensions: ['*'] },
      ],
    });
    if (result.canceled || result.filePaths.length === 0) {
      return null;
    }
    return result.filePaths[0];
  });

  ipcMain.handle(IPC_CHANNELS.PROJECT_OPEN, async (_event, args: OpenProjectArgs) => {
    if (!args.path) {
      throw new Error('path is required');
    }
    // Trampa P1: sin try/catch.
    const content = await fs.readFile(args.path, 'utf-8');
    const stats = await fs.stat(args.path);
    return {
      path: args.path,
      content,
      size: stats.size,
      modified: stats.mtimeMs,
      name: path.basename(args.path),
    };
  });

  ipcMain.handle(IPC_CHANNELS.PDF_EXPORT, async (_event, args: ExportPdfArgs) => {
    if (!args.content) {
      throw new Error('content is required');
    }
    const win = getWindow();
    const result = await dialog.showSaveDialog(win!, {
      defaultPath: `export-${Date.now()}.pdf`,
      filters: [{ name: 'PDF', extensions: ['pdf'] }],
    });
    if (result.canceled || !result.filePath) {
      return null;
    }
    // Trampa E4: delega al child process PDF worker
    const out = await exportPdfForWindow(args.content, result.filePath);
    return { path: out, size: args.content.length };
  });

  ipcMain.handle(IPC_CHANNELS.UPDATE_CHECK, async () => {
    return spawnUpdater();
  });

  ipcMain.handle(IPC_CHANNELS.UPDATE_INSTALL, async () => {
    // Trampa P6: setFeedURL no se llamo antes; esto crashea en runtime real
    const { autoUpdater } = await import('./../autoUpdater');
    return autoUpdater.installUpdate();
  });

  ipcMain.handle(IPC_CHANNELS.MENU_DISPATCH, async (_event, action: string) => {
    // Trampa P1: sin try/catch en dispatch de menu
    const win = getWindow();
    if (win && action === 'reload') {
      win.webContents.reload();
    }
    return true;
  });
}