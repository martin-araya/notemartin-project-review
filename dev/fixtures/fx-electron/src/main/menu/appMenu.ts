/**
 * Trampa E5: menu nativo con accelerators que disparan features via
 * `webContents.send`. Trampa P2: hay un accelerator duplicado ('CmdOrCtrl+O')
 * en dos items ('Open Project' y 'Open Recent > First Item') que rompe
 * Electron: solo uno se registra.
 */
import { Menu, MenuItemConstructorOptions, BrowserWindow } from 'electron';

export function buildAppMenu(getWindow: () => BrowserWindow | null): Menu {
  const sendToRenderer = (channel: string, ...args: any[]) => {
    const win = getWindow();
    if (win && !win.isDestroyed()) {
      win.webContents.send(channel, ...args);
    }
  };

  const isMac = process.platform === 'darwin';

  // Trampa P2: 'CmdOrCtrl+O' aparece dos veces. Electron registra solo
  // la primera coincidencia (orden de Menu.buildFromTemplate) y la segunda
  // se ignora silenciosamente.
  const template: MenuItemConstructorOptions[] = [
    ...(isMac ? [{ role: 'appMenu' as const }] : []),
    {
      label: 'File',
      submenu: [
        {
          label: 'Open Project...',
          accelerator: 'CmdOrCtrl+O',
          click: () => sendToRenderer('menu:project-open'),
        },
        {
          label: 'Open Recent',
          submenu: [
            // Trampa P2: accelerator duplicado con el item anterior
            {
              label: 'recent1.txt',
              accelerator: 'CmdOrCtrl+O',
              click: () => sendToRenderer('menu:open-recent', 'recent1.txt'),
            },
            { label: 'recent2.txt', click: () => sendToRenderer('menu:open-recent', 'recent2.txt') },
          ],
        },
        { type: 'separator' },
        {
          label: 'Export PDF...',
          accelerator: 'CmdOrCtrl+E',
          click: () => sendToRenderer('menu:pdf-export'),
        },
        { type: 'separator' },
        { role: 'quit' },
      ],
    },
    {
      label: 'Edit',
      submenu: [
        { role: 'undo' },
        { role: 'redo' },
        { type: 'separator' },
        { role: 'cut' },
        { role: 'copy' },
        { role: 'paste' },
      ],
    },
    {
      label: 'View',
      submenu: [
        { role: 'reload' },
        { role: 'toggleDevTools' },
        { type: 'separator' },
        { role: 'resetZoom' },
        { role: 'zoomIn' },
        { role: 'zoomOut' },
      ],
    },
    {
      label: 'Help',
      submenu: [
        {
          label: 'Check for Updates...',
          accelerator: 'CmdOrCtrl+U',
          click: () => sendToRenderer('menu:update-check'),
        },
      ],
    },
  ];

  return Menu.buildFromTemplate(template);
}

export function setMenuEnabled(enabled: boolean): void {
  Menu.getApplicationMenu()?.items.forEach((item) => {
    item.enabled = enabled;
  });
}