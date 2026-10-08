/**
 * Trampa E4: child process (fork) para export PDF.
 * Mas simple que utilityProcess; suficiente para un PDF.
 */
import { fork } from 'child_process';
import path from 'path';

export function exportPdfForWindow(content: string, outputPath: string): Promise<string> {
  return new Promise((resolve, reject) => {
    const workerPath = path.join(__dirname, '..', '..', 'workers', 'pdf-worker.js');
    const child = fork(workerPath, [outputPath], {
      stdio: ['ignore', 'pipe', 'pipe', 'ipc'],
    });
    child.send({ kind: 'render', content });
    child.on('message', (msg: any) => {
      if (msg && msg.kind === 'done') {
        resolve(msg.path);
      } else if (msg && msg.kind === 'error') {
        reject(new Error(msg.message));
      }
    });
    child.on('error', (err) => reject(err));
  });
}