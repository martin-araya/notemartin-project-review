// Trampa E05: build tag `//go:build legacy`.
//
// Trampa S01: este archivo define una ruta legacy que solo se compila
// con `-tags legacy`. No se usa en runtime; la skill debe detectarlo
// via grep del build tag.
////go:build legacy
// +build legacy

package http

import (
	"encoding/json"
	"io"
	"net/http"
)

func (h *Handlers) LegacyExportHandler(w http.ResponseWriter, r *http.Request) {
	// Handler legacy: solo se compila con `-tags legacy`.
	// La trampa es que este codigo existe pero no se invoca en runtime.
	out := map[string]interface{}{
		"legacy": true,
		"status": "deprecated",
	}
	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(io.Discard).Encode(out)
}
