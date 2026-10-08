import { app, BrowserWindow } from 'electron';

import { registerAppProtocol } from './protocol/appProtocol';
import { buildAppMenu } from './menu/appMenu';
import { registerIpcHandlers } from './ipc/handlers';

let mainWindow: BrowserWindow | null = null;

function getMainWindow(): BrowserWindow | null {
  return mainWindow && !mainWindow.isDestroyed() ? mainWindow : null;
}

// Trampa E5 + trampa P5: protocolo debe registrarse ANTES de app.ready.
registerAppProtocol();

app.whenReady().then(() => {
  const { createMainWindow } = require('./windows');
  mainWindow = createMainWindow();
  registerIpcHandlers(getMainWindow);
  const { Menu } = require('electron');
  Menu.setApplicationMenu(buildAppMenu(getMainWindow));
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    const { createMainWindow } = require('./windows');
    mainWindow = createMainWindow();
  }
});