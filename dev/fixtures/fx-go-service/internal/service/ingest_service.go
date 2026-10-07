// Package service contiene la logica de negocio de fx-go-service.
package service

import (
	"context"
	"log"
	"time"

	"fx-go-service/internal/domain"
)

type IngestService struct {
	repo domain.EventRepository
}

// NewIngestService construye un IngestService contra el repositorio.
func NewIngestService(repo domain.EventRepository) *IngestService {
	return &IngestService{repo: repo}
}

// Ingest procesa un evento: lo guarda y opcionalmente dispara una
// notificacion. Aqui solo persiste.
func (s *IngestService) Ingest(ctx context.Context, e *domain.Event) error {
	if e.Type == "" {
		return ErrEmptyType
	}
	if e.CreatedAt.IsZero() {
		e.CreatedAt = time.Now().UTC()
	}
	_, err := s.repo.Insert(ctx, e)
	if err != nil {
		log.Printf("ingest: %v", err)
		return err
	}
	return nil
}

// ErrEmptyType se devuelve cuando el evento no tiene tipo.
var ErrEmptyType = errEmptyType("event type is required")

type errEmptyType string

func (e errEmptyType) Error() string { return string(e) }
