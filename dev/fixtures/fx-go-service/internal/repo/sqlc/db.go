// Codigo generado por sqlc (trampa E03: //go:generate).
//
// NO EDITAR A MANO. Regenerar con `sqlc generate` desde la raiz
// del proyecto, despues de `go install github.com/sqlc-dev/sqlc/cmd/sqlc@latest`.
//
// Las queries en queries.sql producen estas funciones:
//
//   - CreateEvent(ctx, arg) error
//   - GetEvent(ctx, id) (Event, error)
//   - ListEventsByType(ctx, arg) ([]Event, error)
//   - CountEventsByType(ctx, type) (int64, error)
//   - DeleteAllEvents(ctx) error
//
// NOTA: este archivo es un STUB para que fx-go-service compile
// sin necesidad de instalar sqlc. En CI/produccion, se regenera
// via `make generate` (o via el comando del Dockerfile).
package sqlc

import "context"

type Event struct {
	ID        int64
	Type      string
	Payload   []byte
	CreatedAt interface{}
}

type CreateEventParams struct {
	Type      string
	Payload   []byte
	CreatedAt interface{}
}

type ListEventsByTypeParams struct {
	Type   string
	Limit  int32
	Offset int32
}

// Stub de las funciones generadas (en runtime, sqlc las genera reales).
func CreateEvent(ctx context.Context, db interface{}, arg CreateEventParams) error {
	return nil
}
func GetEvent(ctx context.Context, db interface{}, id int64) (Event, error) {
	return Event{}, nil
}
func ListEventsByType(ctx context.Context, db interface{}, arg ListEventsByTypeParams) ([]Event, error) {
	return nil, nil
}
func CountEventsByType(ctx context.Context, db interface{}, eventType string) (int64, error) {
	return 0, nil
}
func DeleteAllEvents(ctx context.Context, db interface{}) error {
	return nil
}
