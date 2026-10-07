// ExportService exporta eventos usando una plantilla embebida.
//
// Trampa E06: el FS de plantillas se embebe via //go:embed al compilar,
// de modo que el binario es autocontenido y la ruta de la plantilla
// no aparece en el filesystem en runtime.
package service

import (
	"context"
	"embed"
	"fmt"
	"text/template"
	"time"

	"fx-go-service/internal/domain"
)

//go:embed templates/*.tmpl
var exportFS embed.FS

type ExportService struct {
	repo     domain.EventRepository
	template *template.Template
}

// NewExportService parsea la plantilla embebida y la guarda.
func NewExportService(repo domain.EventRepository) (*ExportService, error) {
	tmpl, err := template.ParseFS(exportFS, "templates/*.tmpl")
	if err != nil {
		return nil, fmt.Errorf("parse template: %w", err)
	}
	return &ExportService{repo: repo, template: tmpl}, nil
}

// Export genera el reporte serializado segun el formato pedido.
func (s *ExportService) Export(ctx context.Context, format string) ([]byte, error) {
	events, err := s.repo.ListByType(ctx, "default", 1000, 0)
	if err != nil {
		return nil, fmt.Errorf("list: %w", err)
	}
	data := map[string]interface{}{
		"GeneratedAt": time.Now().UTC().Format(time.RFC3339),
		"Count":       len(events),
		"Events":      events,
		"Format":      format,
	}
	var buf []byte
	w := &byteWriter{buf: &buf}
	if err := s.template.ExecuteTemplate(w, "header", data); err != nil {
		return nil, fmt.Errorf("exec header: %w", err)
	}
	if err := s.template.ExecuteTemplate(w, "row", data); err != nil {
		return nil, fmt.Errorf("exec row: %w", err)
	}
	return *w.buf, nil
}

// byteWriter envuelve un []byte para implementar io.Writer.
type byteWriter struct {
	buf *[]byte
}

func (w *byteWriter) Write(p []byte) (int, error) {
	*w.buf = append(*w.buf, p...)
	return len(p), nil
}
