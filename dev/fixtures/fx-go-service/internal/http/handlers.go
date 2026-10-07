// Package http contiene los handlers HTTP y el setup de chi.
//
// Trampa E04: el router chi expone el worker pool via el endpoint
// POST /events/submit que encola un job.
package http

import (
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"time"

	"fx-go-service/internal/domain"
	"fx-go-service/internal/service"
	"fx-go-service/internal/worker"

	"github.com/go-chi/chi/v5"
)

type Handlers struct {
	ingest    *service.IngestService
	aggregate *service.AggregateService
	export    *service.ExportService
	pool      *worker.Pool
}

func (h *Handlers) Routes() http.Handler {
	r := chi.NewRouter()
	r.Post("/events", h.IngestEvent)
	r.Get("/events", h.ListEvents)
	r.Get("/aggregate", h.GetAggregate)
	r.Get("/export", h.ExportData)
	r.Post("/events/submit", h.SubmitJob)
	return r
}

// IngestEvent crea un evento.
func (h *Handlers) IngestEvent(w http.ResponseWriter, r *http.Request) {
	var payload struct {
		Type    string          `json:"type"`
		Payload json.RawMessage `json:"payload"`
	}
	if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid_json"})
		return
	}
	if payload.Type == "" {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "type_required"})
		return
	}
	e := &domain.Event{
		Type:      payload.Type,
		Payload:   payload.Payload,
		CreatedAt: time.Now().UTC(),
	}
	if err := h.ingest.Ingest(r.Context(), e); err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "ingest_failed"})
		return
	}
	writeJSON(w, http.StatusCreated, map[string]interface{}{"status": "created", "type": e.Type})
}

// ListEvents lista los eventos por tipo.
func (h *Handlers) ListEvents(w http.ResponseWriter, r *http.Request) {
	t := r.URL.Query().Get("type")
	events, err := h.aggregate.ListByType(r.Context(), t, 50, 0)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "list_failed"})
		return
	}
	writeJSON(w, http.StatusOK, events)
}

// GetAggregate devuelve el aggregate computado.
func (h *Handlers) GetAggregate(w http.ResponseWriter, r *http.Request) {
	agg, err := h.aggregate.Compute(r.Context())
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "compute_failed"})
		return
	}
	writeJSON(w, http.StatusOK, agg)
}

// ExportData devuelve el export serializado.
func (h *Handlers) ExportData(w http.ResponseWriter, r *http.Request) {
	format := r.URL.Query().Get("format")
	if format == "" {
		format = "json"
	}
	out, err := h.export.Export(r.Context(), format)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "export_failed"})
		return
	}
	w.Header().Set("Content-Type", "text/plain")
	_, _ = io.WriteString(w, string(out))
}

// SubmitJob encola un job en el worker pool.
func (h *Handlers) SubmitJob(w http.ResponseWriter, r *http.Request) {
	var body struct {
		JobID int `json:"job_id"`
	}
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid_json"})
		return
	}
	if body.JobID <= 0 {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "job_id_required"})
		return
	}
	h.pool.Submit(body.JobID)
	writeJSON(w, http.StatusAccepted, map[string]interface{}{"queued": true})
}

func writeJSON(w http.ResponseWriter, status int, v interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(v)
}

var _ = errors.New
var _ = fmt.Sprintf
