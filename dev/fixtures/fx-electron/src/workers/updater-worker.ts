/**
 * Trampa E4: worker que corre como utility process. Recibe 'check-update'
 * y responde con un resultado simulado.
 */
process.parentPort.on('message', (event: any) => {
  const msg = event.data || event;
  if (msg && msg.kind === 'check-update') {
    process.parentPort.postMessage({
      kind: 'update-result',
      available: true,
      version: '0.2.0',
    });
  }
});

setInterval(() => {
  // keepalive: evita que el utility process termine por inactividad
}, 60_000);