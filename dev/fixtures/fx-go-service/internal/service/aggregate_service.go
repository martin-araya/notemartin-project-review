// AggregateService computa aggregations sobre los eventos.
package service

import (
	"context"

	"fx-go-service/internal/domain"
)

type AggregateService struct {
	repo domain.EventRepository
}

// NewAggregateService construye un AggregateService contra el repo.
func NewAggregateService(repo domain.EventRepository) *AggregateService {
	return &AggregateService{repo: repo}
}

// ListByType es un helper de compatibilidad que delega al repo.
// La firma difiere de domain.EventRepository.ListByType en el
// nombre del parametro de tipo (trampa P03: implicit interface
// mismatch si el caller espera otra firma).
func (s *AggregateService) ListByType(ctx context.Context, eventType string, limit, offset int) ([]*domain.Event, error) {
	return s.repo.ListByType(ctx, eventType, limit, offset)
}

// Compute agrupa los eventos por tipo y devuelve los conteos.
func (s *AggregateService) Compute(ctx context.Context) ([]domain.Aggregate, error) {
	// Lista de tipos "conocidos" para simplificar. En produccion se
	// usaria un SELECT DISTINCT.
	knownTypes := []string{"user.created", "user.deleted", "order.placed", "page.view"}
	out := make([]domain.Aggregate, 0, len(knownTypes))
	for _, t := range knownTypes {
		n, err := s.repo.CountByType(ctx, t)
		if err != nil {
			return nil, err
		}
		if n == 0 {
			continue
		}
		out = append(out, domain.Aggregate{
			Type:  t,
			Count: n,
		})
	}
	return out, nil
}
