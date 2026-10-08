declare const window: { api: any };

const statusEl = document.getElementById('status')!;
const outputEl = document.getElementById('output')!;

function setStatus(text: string): void {
  statusEl.textContent = text;
}

function show(text: string): void {
  outputEl.textContent = text;
}

document.getElementById('open-btn')!.addEventListener('click', async () => {
  setStatus('Abriendo dialog...');
  const path = await window.api.openProjectDialog();
  if (!path) {
    setStatus('Cancelado');
    return;
  }
  const project = await window.api.openProject({ path });
  show(JSON.stringify(project, null, 2));
  setStatus('Cargado');
});

document.getElementById('pdf-btn')!.addEventListener('click', async () => {
  setStatus('Exportando...');
  const content = outputEl.textContent ?? '';
  const result = await window.api.exportPdf({ content });
  if (!result) {
    setStatus('Cancelado');
    return;
  }
  show(`PDF: ${result.path} (${result.size} bytes)`);
  setStatus('Exportado');
});

document.getElementById('update-btn')!.addEventListener('click', async () => {
  setStatus('Verificando updates...');
  const result = await window.api.checkUpdate();
  show(JSON.stringify(result, null, 2));
  setStatus(result.available ? 'Update disponible' : 'Al dia');
});

window.api.onMenuDispatch((action: string) => {
  setStatus(`Menu: ${action}`);
});