/**
 * Trampa E4: child process que genera PDFs.
 * Implementacion stub: copia el contenido como texto plano en un .pdf.
 */
const fs = require('fs');
const path = require('path');

const outputPath = process.argv[2];
let input = '';

process.on('message', (msg) => {
  if (msg && msg.kind === 'render') {
    input = msg.content || '';
    const pdfBody = `%PDF-1.4\n%mock-pdf\n${input}\n%%EOF`;
    fs.writeFile(outputPath, pdfBody, (err: any) => {
      if (err) {
        process.send({ kind: 'error', message: String(err) });
              } else {
        process.send({ kind: 'done', path: outputPath });
      }
    });
  }
});