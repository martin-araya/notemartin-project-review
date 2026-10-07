// Interfaces del dominio (trampa E01: implementacion estructural).
//
// Las interfaces aqui declaradas son implementadas por los structs
// en internal/repo/sqlite sin la keyword 'implements'. La skill debe
// verificar el matching de signatures (Insert, ListByType, etc.)
// entre estas interfaces y los metodos del struct.
package domain

import "context"

type EventRepository interface {
	Insert(ctx context.Context, e *Event) (int64, error)
	GetByID(ctx context.Context, id int64) (*Event, error)
	ListByType(ctx context.Context, eventType string, limit, offset int) ([]*Event, error)
	CountByType(ctx context.Context, eventType string) (int64, error)
	DeleteAll(ctx context.Context) error
}

type Exporter interface {
	Export(ctx context.Context, format string) ([]byte, error)
}
